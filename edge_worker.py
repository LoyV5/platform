import queue
import sys
import time
import string
import random
import numpy as np
from loguru import logger
from concurrent import futures
import json
import edge_globals
from tools.read_config import read_config
from local.preprocessor import preprocess
from frontend_server.offloading import send_frame
from tools.transfer_files_tool import transfer_array_and_str
#分了目标检测和图像分类两类任务，以后会删掉图像分类任务
from model_manager import object_detection, image_classification


# the video frame handler of the forwarding server
frame_handler = read_config("flask-url", "video_frame_url")

# generate the id for a task
def id_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ThreadPoolExecutorWithQueueSizeLimit(futures.ThreadPoolExecutor):
    def __init__(self, maxsize=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._work_queue = queue.Queue(maxsize=maxsize)


class Task:
    #ret为返回的结果类型img/txt
    def __init__(self, task_id, frame, serv_type, t_start, res_return,cmprs):
        self.task_id = task_id       #id
        self.frame = frame           #帧数据
        self.serv_type = serv_type   #任务类型
        self.t_start = t_start       #任务创建时间
        self.t_trans = None          #任务传输时间
        self.t_wait = None           #任务等待时间
        self.t_inf = None            #任务推理时间
        self.t_all = None            #任务处理总时间，应该等于trans+wait+inf
        self.ret=res_return          #返回结果类型
        self.compress=cmprs          #是否压缩
        self.selected_model = None   #选择的yolo模型
        self.location = None         #处理位置,本地or云
        self.new_size = None         #预处理分辨率
        self.new_qp = None           #预处理qp


def local_inference(task):
    """local inference for a video frame"""
    
    #本地推理

    model = edge_globals.loaded_model[task.selected_model]
    #根据任务类型修改推理方式
    if task.serv_type == edge_globals.OBJECT_DETECTION:
        #输入帧、模型、iou阈值
        #返回结果对象 
        result,inftime = object_detection.object_detection_api(task.frame, model, threshold=0.7)
        return result,inftime
    #图像分类任务，暂时弃用
    if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
        result,inftime = image_classification.image_classification(task.frame, model)
        return result,inftime

#本地任务
def local_worker(task_queue):
    
    while True:
         
        # get a task from the queue
        try:
            #这里从队列中拿出了任务，从这里记录等待时间
            task = task_queue.get(block=True)
            task.t_wait=time.time()-task.t_start
            edge_globals.sys_info.local_pending_task -= 1

        #这个是视频帧全都处理完了，返回本地平均处理时延
        except Exception:
            average_local_delay = np.average([p.value for p in edge_globals.sys_info.local_delay])
            #logger.info("average local delay:"+str(average_local_delay))
            sys.exit()
        else:
            # locally process the task
            
            result,task.t_inf = local_inference(task)

            #总处理时间
            processing_delay = task.t_wait + task.t_inf

            task.t_all=processing_delay

            logger.info("local_processing_delay:"+str(processing_delay))

            # record the processing delay
            # edge_globals.sys_info.append_local_delay(t_start, processing_delay)

            if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
                logger.info("image classification result:"+result)
            elif task.serv_type == edge_globals.OBJECT_DETECTION:
                logger.info("object detection works well! please go to info_store/handled_result to check.")
                #本地推理只输出txt，要输出图片的话解除下面这行的注释
                #edge_globals.datastore.store_image(result[0].plot())
                edge_globals.datastore.store_txt(result)
                #混合保存时延、处理位置等数据，最终导出为json
                edge_globals.datastore.store_json(task)
                

#卸载
def offload_worker(task):
    #预处理函数(只有上传到云端的才做预处理)
    #预处理目前只拿来改变分辨率
    #task = preprocess(task)

    #读取文件大小
    file_size = sys.getsizeof(task.frame)

    # send the video frame to the server
    
    try:
        #尝试发送帧,frame_handler是forward服务器地址
        result_dict, start_time, processing_delay, arrive_transfer_server_time = \
            send_frame(frame_handler, task.frame, task.selected_model,task.ret,task.compress)
        t_end = time.time()
    except Exception as err:
        logger.exception("offloading error")
    else:
        total_processing_delay = t_end - task.t_start
        # record the bandwidth and the processing delay
        # 记录带宽和处理时延

        bandwidth = file_size / arrive_transfer_server_time
        edge_globals.sys_info.append_bandwidth(task.t_start, bandwidth)
        edge_globals.sys_info.append_offload_delay(task.t_start, total_processing_delay)

        task.t_trans=arrive_transfer_server_time

        task.t_inf=float(result_dict["inftime"])

        task.t_wait=total_processing_delay-task.t_trans-task.t_inf

        task.t_all=total_processing_delay

        #两种不同任务类型

        if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
            result = result_dict["prediction"]
            logger.info("offload:"+result)
    
        elif task.serv_type == edge_globals.OBJECT_DETECTION:
    
            frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))

            if task.ret=='1':
                frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
                edge_globals.datastore.store_image(frame_handled)
                edge_globals.datastore.store_json(task)
                logger.info("cloud process image well!")

            #处理返回的txt数据
            else:
                texts=json.loads(result_dict["result"])
                edge_globals.datastore.store_txtjson(texts)
                edge_globals.datastore.store_json(task)
                logger.info("cloud process image well!")



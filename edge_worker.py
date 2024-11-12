import queue
import sys
import time
import string
import random
import numpy as np
from loguru import logger
from concurrent import futures

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

    def __init__(self, task_id, frame, serv_type, t_start):
        self.task_id = task_id
        self.frame = frame
        self.serv_type = serv_type
        self.t_start = t_start
        self.selected_model = None
        self.location = None
        self.new_size = None
        self.new_qp = None


def local_inference(task):
    """local inference for a video frame"""
    
    #本地推理

    model = edge_globals.loaded_model[task.selected_model]
    #根据任务类型修改推理方式
    if task.serv_type == edge_globals.OBJECT_DETECTION:
        #输入帧、模型、iou阈值
        #返回结果对象 
        result = object_detection.object_detection_api(task.frame, model, threshold=0.7)
        return result
    #图像分类任务，暂时弃用
    if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
        result = image_classification.image_classification(task.frame, model)
        return result

#本地混合任务
def local_worker(task_queue):
    
    while True:
         
        # get a task from the queue
        try:
            task = task_queue.get(block=True)
            edge_globals.sys_info.local_pending_task -= 1
        except Exception:
            average_local_delay = np.average([p.value for p in edge_globals.sys_info.local_delay])
            # logger.info("average local delay:"+str(average_local_delay))
            sys.exit()
        else:
            # locally process the task
            t_start = task.t_start
            result = local_inference(task)
            t_end = time.time()
            processing_delay = t_end - t_start

            # logger.info("local_processing_delay:"+str(processing_delay))
            # record the processing delay
            edge_globals.sys_info.append_local_delay(t_start, processing_delay)

            if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
                logger.info("image classification result:"+result)
            elif task.serv_type == edge_globals.OBJECT_DETECTION:
                logger.info("object detection works well! please go to info_store/handled_result to check.")
                edge_globals.datastore.store_image(result[0].plot())
                edge_globals.datastore.store_txt(result)
                

#卸载
def offload_worker(task):
    #预处理函数(只有上传到云端的才做预处理)
    #如果发不出去就禁用预处理
    #task = preprocess(task)

    #读取文件大小
    file_size = sys.getsizeof(task.frame)

    # send the video frame to the server
    
    try:
        #尝试发送帧,frame_handler是forward服务器地址
        result_dict, start_time, processing_delay, arrive_transfer_server_time = \
            send_frame(frame_handler, task.frame, task.selected_model)
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

        #两种不同任务类型

        if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
            result = result_dict["prediction"]
            logger.info("offload:"+result)
    
        elif task.serv_type == edge_globals.OBJECT_DETECTION:
    
            frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
            frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
            edge_globals.datastore.store_image(frame_handled)
            logger.info("cloud process image well!")

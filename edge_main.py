import os
import sys
import time
import argparse
import queue
import threading
import edge_globals
import numpy as np
from loguru import logger
from local.sys_info import SysInfo
from tools.read_config import read_config
from local.local_store import DataStore
from local.video_reader import VideoReader
from local.decision_engine import DecisionEngine
from model_manager.model_cache import load_models
from config.model_info import edge_object_detection_model
from edge_worker import local_worker, offload_worker, Task, id_gen, ThreadPoolExecutorWithQueueSizeLimit

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    #参数设置
    #-f 文件
    group.add_argument('-f', '--file', help="input video file or local camera")
    #-r rtsp流
    group.add_argument('-r', '--rtsp', help="RTSP camera", action='store_true')
    #设置任务类型
    parser.add_argument(
        '-s', '--serv', type=int, default=1,
        help="input service demand, 1 for OBJECT_DETECTION",
    )
    #设置云服务器返回的是图片还是txt,0返回txt,1返回图片，默认0
    parser.add_argument('-t', '--ret', type=str, default='0' , help="result return")

    #是否压缩图片，以jpeg方式发送,0以png发送，1以jpeg发送，默认0
    parser.add_argument('-c', '--compress', type=str, default='0', help="post png/jpeg")

    #帧读取间隔
    parser.add_argument('-i', '--interval', type=int, help="interval between reading two frames in ms", required=True)
    args = parser.parse_args()

    #生成日志文件

    logger.add("log/client_{time}.log", level="INFO")

    file_type = edge_globals.IMAGE_TYPE
    serv_type = 1  # args.serv
    INTERVAL = args.interval / 1000.0  # convert into seconds
    input_file = args.file
    res_return = args.ret
    cmprs = args.compress
    if input_file is not None:
        if os.path.isfile(input_file) is False and input_file.isdigit() is False:
            logger.error("input video file or local camera does not exist")
            sys.exit()
        elif input_file.isdigit():
            input_file = int(input_file)

    if input_file is None and args.rtsp is False:
        logger.error("select either video file or RTSP camera")
        sys.exit()

    # 从配置文件中获取控制策略
    edge_policy = read_config("edge-setting", "control_policy")
    # 将视频分析模型加载到内存中 (本地推理)
    # 非云端的话进行本地推理
    if edge_policy != "always_cloud_lowest_delay":
        logger.info("local models are loading...")
        edge_globals.loaded_model = load_models(edge_object_detection_model)
        logger.info("local models have loaded!")
    # create the objects for video reading, decision making, and information management
    # 创建用于视频读取、决策和信息管理的对象
    reader = VideoReader(input_file, args.rtsp)
    edge_globals.sys_info = SysInfo()
    #根据终端设备当前资源信息做决策
    decision_engine = DecisionEngine(edge_globals.sys_info)
    #加载结果输出函数
    edge_globals.datastore = DataStore()
    # start the thread pool for processing offloading requests
    # 启动线程池以处理卸载请求
    # 读取config中的队列长度限制
    WORKER_NUM = int(read_config("edge-setting", "worker_number"))
    executor = ThreadPoolExecutorWithQueueSizeLimit(max_workers=WORKER_NUM)

    # the queue for local processing task passing
    # 本地处理任务传递队列
    task_queue = queue.Queue(int(read_config("edge-setting", "queue_maxsize")))
    # start the thread for local inference
    # 启动本地推理线程
    local_processor = threading.Thread(target=local_worker, args=(task_queue,))
    local_processor.start()

    # n = 0
    # read frames from video file or camera in loop
    # 从视频文件或相机循环中读取帧
    while True:

        frame = reader.read_frame()
        if frame is None:
            executor.shutdown(wait=True)
            local_processor.join(timeout=20)
            #如果完全不卸载到云端的话可能出现除法警告
            cloud_average_process_delay = np.average([p.value for p in edge_globals.sys_info.offload_delay])
            logger.info("Service come over!")
            sys.exit()

        # obtain the CPU and memory usage
        edge_globals.sys_info.update_local_utilization()

        # create the inference as a task
        task_id = id_gen()
        t_start = time.time()
        task = Task(task_id, frame, serv_type, t_start, res_return, cmprs)

        # make decision on video frame processing
        # 视频帧处理决策
        task = decision_engine.get_decision(edge_policy, task)

        # local processing on the edge
        # 边缘本地处理
        if task.location == edge_globals.LOCAL:

            task_queue.put(task, block=True)
            edge_globals.sys_info.local_pending_task += 1

        # offload to the cloud for processing
        # 卸载到云端进行处理
        elif task.location == edge_globals.OFFLOAD:
            #卸载代码
            executor.submit(offload_worker, task)

        t_end = time.time()

        #如果返回时间小于帧读取间隔，则等待到下个帧读取
 
        if t_end - t_start < INTERVAL:
            dur = INTERVAL - (t_end - t_start)
            time.sleep(dur)

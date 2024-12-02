#!/usr/bin/env python
# encoding: utf-8

from tools import make_request
from tools.transfer_files_tool import transfer_array_and_str
from loguru import logger
import cv2


def send_frame(url, frame, selected_model,ret,compress):
    """Send the image frame to the transfer server.

    Send the image frame to the transfer server, and get the result of server.
    At the same time, calculate the time of total processing and arrive transfer server delay.

    :param url: transfer server's url
    :param frame: image frame to send to server
    :param selected_model: model name to send to server
    :return: result_dict: result dict returned from server
             start_time: the start time of calculating the time
             processing_delay: total processing time
             arrive_transfer_server_time: the delay between client and transfer server
    """
    #image.shape输出(w,h,channels)数字列表
    frame_shape = frame.shape
    #转换成(w,h,channels)的字符串
    frame_shape_str = f"({','.join(map(str, frame_shape))})"
    
    #jpeg编码，默认质量等级
    if compress=='1':
        success,frame=cv2.imencode('.jpg',frame)

    img_str = transfer_array_and_str(frame, "up")
    msg_dict = {
        "selected_model": selected_model,
        "frame_shape": frame_shape_str,
        "frame": img_str,
        "ret":ret,
        "compress":compress
    }
    try:
        result_dict, start_time, processing_delay, arrive_transfer_server_time = make_request.make_request(url, **msg_dict)
    except Exception as err:
        logger.exception("servers return nothing")
    else:
        return result_dict, start_time,  processing_delay, arrive_transfer_server_time


# video file interface
# 被弃用
def process_video_file(url, input_file):

        response = make_request.make_request(url)
        video = response.read().decode('utf-8')
        # if selected_model == "image classification":
        #     print(video)
        # else:
        #     save_file(video, input_file)

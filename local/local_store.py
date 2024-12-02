#!/usr/bin/env python
# encoding: utf-8

import os
import cv2
import datetime
import edge_globals
from loguru import logger
import json


class DataStore:
    """Store results locally.

    According to the requirements, LocalStore stores the input video frame
    as image or video in local directory.
    """

    def __init__(self, store_type=None):
        time = datetime.datetime.now()
        store_path = os.path.join(os.path.dirname(__file__), "../info_store/handled_result")
        self.n = 0
        self.dicts=[]
        self.server_info=[]
        self.result_store_location = os.path.join(
            store_path, time.strftime('%a%b%d%H%M')
        )
        if store_type == edge_globals.VIDEO_TYPE:
            video_name = time.strftime('%a%b%d%H%M') + ".mp4"
            self.out = cv2.VideoWriter(
                video_name, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480)
            )

    def store_image(self, frame):
        """Store frame as image

        :param frame: image which will be stored, type numpy.narray
        :return: None
        """
        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            image_path = os.path.join(self.result_store_location, "out"+str(self.n)+".png")
            cv2.imwrite(image_path, frame)
            self.n += 1
        except Exception as err:
            print("save image fail:", err)

    #新增，用于存放本地检测后的txt数据
    def store_txt(self, result):
        """
        保存检测结果的txt数据
        """
        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            txt_path = os.path.join(self.result_store_location, "out"+str(self.n)+".txt")
            result[0].save_txt(txt_path)
            self.n += 1
        except Exception as err:
            print("save txt fail:", err)
    
    #新增，用于存放服务器检测后返回的txt数据(以nparray数组列表形式返回)
    def store_txtjson(self, texts):
        """
        保存检测结果的txt数据
        """
        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            txt_path = os.path.join(self.result_store_location, "out"+str(self.n)+".txt")
            with open(txt_path, 'w') as f:
                f.writelines(text + "\n" for text in texts)
            self.n += 1
        except Exception as err:
            print("save txt fail:", err)

    #新增，用于存放服务器检测后返回的txt数据(以nparray数组列表形式返回)
    #
    def store_json(self, task):
        """
        以json形式保存时延等结果数据
        """

        data = {
            "id":task.task_id,
            "trans_time":task.t_trans,
            "wait_time":task.t_wait,
            "inf_time":task.t_inf,
            "proc_time":task.t_all
        }

        self.dicts.append(data)

        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            json_path = os.path.join(self.result_store_location, "output.json")
            # 创建json并写入
            with open(json_path, "w") as f_new:
                json.dump(self.dicts,f_new,indent=4)
                
        except Exception as err:
            print("save json fail:", err)

    #新增，用于存放轮询回来的服务器数据
    def store_info(self, info):
        """
        以json形式保存服务器数据
        """

        self.server_info.append(info)

        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            json_path = os.path.join(self.result_store_location, "server_info.json")
            # 创建json并写入
            with open(json_path, "w") as f:
                json.dump(self.server_info,f,indent=4)
                
        except Exception as err:
            print("save json fail:", err)
    
  
    def store_video(self, frame):
        """Write a image frame into a video file.

        :param frame: image which will be written, type numpy.ndarray
        :return: None
        """
        try:
            self.out.write(frame)
        except Exception as err:
            print("write frame into video fail", err)




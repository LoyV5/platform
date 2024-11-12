#!/usr/bin/env python
# encoding: utf-8

import os
import cv2
import datetime
import edge_globals
from loguru import logger


class DataStore:
    """Store results locally.

    According to the requirements, LocalStore stores the input video frame
    as image or video in local directory.
    """

    def __init__(self, store_type=None):
        time = datetime.datetime.now()
        store_path = os.path.join(os.path.dirname(__file__), "../info_store/handled_result")
        self.n = 0
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

    #新增，用于存放检测后的txt数据
    def store_txt(self, result):
        """
        保存检测结果的txt数据
        """
        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            txt_path = os.path.join(self.result_store_location, "out"+str(self.n)+".txt")
            result[0].save_txt(txt_path)
            #self.n += 1
        except Exception as err:
            print("save txt fail:", err)

    def store_video(self, frame):
        """Write a image frame into a video file.

        :param frame: image which will be written, type numpy.ndarray
        :return: None
        """
        try:
            self.out.write(frame)
        except Exception as err:
            print("write frame into video fail", err)




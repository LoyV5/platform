import cv2
from tools.read_config import read_config


class VideoReader:
    def __init__(self, input_source=None, rtsp_camera=False):
        self.input_source = None
        if input_source is not None:
            self.input_source = input_source
        elif rtsp_camera is True:
            account = read_config("camera-info", "account")
            password = read_config("camera-info", "password")
            ip_address = read_config("camera-info", "ip_address")
            channel = int(read_config("camera-info", "channel"))
            self.input_source = "rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" \
                                % (account, password, ip_address, channel)
        self.cap = cv2.VideoCapture(self.input_source)

    def read_frame(self,imgsz=None):
        if self.cap.isOpened():
            #读取一帧
            ret, frame = self.cap.read()
            if ret:
                #按给定的分辨率调整大小，默认不改
                if imgsz is not None:
                    frame=cv2.resize(frame, imgsz,interpolation=cv2.INTER_AREA)
                return frame
            self.cap.release()
            return None
        return None

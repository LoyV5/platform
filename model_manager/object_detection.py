from PIL import Image
from loguru import logger
from ultralytics import YOLO

def object_detection_api(img, model, threshold=0.7):

    results = model(img,save=False,save_txt=False,show=False,iou=threshold)
    #返回的是yolov8的结果对象
    
    #也可以只取出标注后的图片传回去
    #res=results[0].plot()

    #返回结果对象

    return results


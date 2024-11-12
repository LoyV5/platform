import os
import sys
import torch
from loguru import logger
from config.model_info import model_lib
from ultralytics import YOLO



#输入模型列表
def load_models(model_list):
    loaded_model = {}
    #模型路径
    weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
    
    for model_name in model_list:
        if model_name in model_lib.keys():
            weight_files_path = os.path.join(weight_folder, model_lib[model_name]['model_path'])
            # 加载模型文件
            model = YOLO(weight_files_path)
            loaded_model[model_name] = model
        else:
            logger.error('model does not exist')
            sys.exit()
    return loaded_model

#选本地最快的
def get_fastest_model(model_list):
    fast_model = None
    min_delay = float('inf')
    for model in model_list:
        if model in model_lib.keys():
            delay = model_lib[model]["tx2_delay"]
            if delay < min_delay:
                fast_model = model
                min_delay = delay
    return fast_model

#选精度最高的，我这里直接指定yolov8x
def get_most_precise_model(model_list):
    
    return "yolov8x"
    precise_model = None
    max_precision = float('-Inf')
    for model in model_list:
        if model in model_lib.keys():
            precision = model_lib[model]['precision']
            if precision > max_precision:
                precise_model = model
                max_precision = precision
    return "retinanet_resnet50_fpn"
    return precise_model



















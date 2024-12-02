#已修改，使用yolov8的所有模型
#tx2为本地计算时延
#cloud为云端计算，均需重新测量
model_lib = {
    'yolov8n': {
        'model_path': 'yolov8n.pt',
        'tx2_delay':   0.18,
        'cloud_delay': 0.009,
        'precision':   None,
        'service_type': 'object_detection'
    },
    'yolov8s': {
        'model_path': 'yolov8s.pt',
        'tx2_delay':  0.39,
        'cloud_delay': 0.009,
        'precision':  None,
        'service_type': 'object_detection'
    },
    'yolov8m': {
        'model_path': 'yolov8m.pt',
        'tx2_delay':  1.57,
        'cloud_delay': 0.012,
        'precision':  None,
        'service_type': 'object_detection'
    },
    'yolov8l': {
        'model_path': 'yolov8l.pt',
        'tx2_delay':   1.65,
        'cloud_delay': 0.017,
        'precision':   None,
        'service_type': 'object_detection'
    },
    'yolov8x': {
        'model_path': 'yolov8x.pt',
        'tx2_delay':  1.77,
        'cloud_delay':  0.032,
        'precision':  None,
        'service_type': 'object_detection'
    },
}

edge_object_detection_model = (
    'yolov8n',
    'yolov8s',
)

cloud_object_detection_model = (
    #'yolov8n',
    'yolov8s',
    'yolov8m',
    #'yolov8l',
    #'yolov8x',
)



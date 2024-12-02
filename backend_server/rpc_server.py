import os
from concurrent import futures
import grpc
import sys
import torch
import backend_globals
from backend_store import DataStore
sys.path.append("../")
from backend_server.model_controller import load_a_model, get_server_utilization, load_model_files_advance
from model_manager import object_detection, image_classification
from backend_server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.transfer_files_tool import transfer_array_and_str
from tools.read_config import read_config
from loguru import logger
from config.model_info import cloud_object_detection_model
from model_manager.model_cache import load_models
import json
import cv2
import argparse


#读取可用模型
object_detection_models = read_config("object-detection")
image_classification_models = read_config("image-classification")
backend_globals.datastore=DataStore()

logger.add("log/grpc-server_{time}.log")

# if torch.cuda.is_available():
#     os.environ["CUDA_VISIBLE_DEVICES"] = "0"

parser = argparse.ArgumentParser()

#yolo模型的input size,需要宽和高w,h
parser.add_argument('-wd', '--width', type=int, default=640, help="input w")
    
parser.add_argument('-ht', '--height', type=int, default=640, help="input h")

args = parser.parse_args()

wid=args.width

hgt=args.height

imgsz=(wid,hgt)

frame_shp=(wid,hgt,3)

str_imgsz= f"({','.join(map(str, frame_shp))})"


class MsgTransferServer(msg_transfer_pb2_grpc.MsgTransferServicer):
    """gRPC server stub.

    This is a gRPC server stub. Get the request from the gRPC client stub,
    process it and return the result, including image frame, load model request, system info and so on.
    """

    def image_processor(self, request, context):
        """Image process interface.

        Get the image process request from the client, process it and return the result.

        """
        selected_model = request.model
        frame = request.frame
        frame_shape = tuple(int(s) for s in request.frame_shape[1:-1].split(","))
        ret=request.ret
        compress=request.compress
        model = backend_globals.loaded_model[selected_model]
        #base64转nparray图片
        img = transfer_array_and_str(frame, 'down')
        #如果是jpeg需要先解码
        if compress=='1':
            img = cv2.imdecode(img,cv2.IMREAD_COLOR)
        
        img = img.reshape(frame_shape)

        msg_reply = image_handler(img, model, selected_model,ret)

        return msg_reply

    def get_server_utilization(self, request, context,imgsz=str_imgsz):
        """Server utilization interface

        Return server utilization to the client.
        """
        server_utilization_reply = get_server_utilization(imgsz)

        return server_utilization_reply

    def get_loaded_models_name(self, request, context):
        """Loaded model name interface

        Return the loaded model names in the server.
        """
        loaded_model_name_reply = msg_transfer_pb2.Loaded_Model_Name_Reply(
            loaded_model_name=str(backend_globals.loaded_model.keys())
        )
        return loaded_model_name_reply

    def load_specified_model(self, request, context):
        """Load specified model interface.

        Load the specified model as the client request.
        """

        specified_model = request.specified_model
        load_a_model(specified_model)
        load_specified_model_reply = msg_transfer_pb2.load_specified_model_Reply()
        return load_specified_model_reply


def image_handler(img, model, selected_model,ret):
    """Image process function

    :param img: image frame
    :param model: loaded model
    :param selected_model: loaded model name
    :return: processed result
    """

    if selected_model in object_detection_models:
        result,inftime = object_detection.object_detection_api(img, model, threshold=0.7,imgsz=imgsz)
        if ret=='1':
            #返回图片
            frame_handled = result[0].plot()

            #在云端默认不存,发txt回本地
            #backend_globals.datastore.store_image(frame_handled)
            #backend_globals.datastore.store_txt(result)

            frame_handled_shape = str(frame_handled.shape)
            img_str = transfer_array_and_str(frame_handled, 'up')
            inftime = str(inftime)
            msg_reply = msg_transfer_pb2.MsgReply(
            result=img_str, frame_shape=frame_handled_shape
            )
        else:
            frame_handled = result[0].plot()
            frame_handled_shape = str(frame_handled.shape)
            inftime = str(inftime)

            #返回txt json
            texts=[]
            for j, d in enumerate(result[0].boxes):
                c = int(d.cls)
                line = (c, * d.xywhn.view(-1))
                texts.append(("%g " * len(line)).rstrip() % line)

            txt_json =json.dumps(texts)
            msg_reply = msg_transfer_pb2.MsgReply(
            result=txt_json, frame_shape=frame_handled_shape, inftime=inftime
            )
        return msg_reply
    else:
        result = image_classification.image_classification(img, model)
        msg_reply = msg_transfer_pb2.MsgReply(
            result=result, frame_shape=""
        )
        return msg_reply


def serve():

    logger.info("grpc server loading...")
    backend_globals.loaded_model = load_models(cloud_object_detection_model)
    logger.info("server models have loaded!")
    MAX_MESSAGE_LENGTH = 256 * 1024 * 1024
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=1),
        maximum_concurrent_rpcs=10,
        options=[
            ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
            ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        ]
    )
    msg_transfer_pb2_grpc.add_MsgTransferServicer_to_server(
      MsgTransferServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("server start!")
    server.wait_for_termination()


if __name__ == '__main__':

    serve()


import sys
from dispatch_policy import random_policy, shortest_queue, lowest_cpu_utilization, pick_input
from frontend_server.grpc_interface import get_grpc_reply
import frontend_globals
from frontend_server.monitor import server_monitor
sys.path.append("../")
from tools.read_config import read_config
from loguru import logger
import json
from flask import Flask, request, jsonify
import time
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

sched = BackgroundScheduler(daemon=True)
sched.add_job(server_monitor, 'interval', seconds=int(read_config("monitor", "monitor_interval")))
sched.start()

logger.add("log/transfer-server_{time}.log")


@app.route('/image_handler', methods=['GET', 'POST'])
def image_handler():
    """Images transfer interface.


    Get info sent from local and transfer it to processing servers,
    then collect the processing result returned from grpc server
    and return the result to the client.

    :return: return_dict
    """
    upload_file = request.get_data()
    info_dict = json.loads(upload_file)
    img_shape = info_dict["frame_shape"]

    server_url = rpc_server_selection("input_size",img_shape)
    #记录服务器当前任务数
    frontend_globals.tasks_number[server_url] += 1
    t1 = time.time()
    try:
        msg_reply = get_grpc_reply(server_url, **info_dict)
    except Exception as err:
        logger.exception("Get result error:", err)
    frontend_globals.tasks_number[server_url] -= 1
    t2 = time.time()
    if msg_reply is None:
        return None
    if msg_reply.frame_shape == "":
        return_dict = {
            "prediction": msg_reply.result,
            "process_time": t2 - t1,
            "inftime":msg_reply.inftime
            }
        return jsonify(return_dict)
    else:
        return_dict = {
            "frame_shape": msg_reply.frame_shape,
            "result": msg_reply.result,
            "process_time": t2 - t1,
            "inftime":msg_reply.inftime
            }
        return jsonify(return_dict)
    
@app.route('/server_info', methods=['GET'])
def server_info():
    info={}

    for grpc_server in frontend_globals.grpc_servers:
        num=frontend_globals.grpc_servers.index(grpc_server)
        info[grpc_server] = {
            "tasks_number":frontend_globals.tasks_number[grpc_server],
            "gpu_usage":frontend_globals.gpu_usage[num],
            "cpu_usage":frontend_globals.cpu_usage[num],
            "memory_usage":frontend_globals.memory_usage[num]
        }
    
    return jsonify(info)
       
def rpc_server_selection(policy,img_shape):
    """Select a grpc server to which info will send.

    :param policy decide the policy of selecting a grpc server
    :return: server url
    """
    if policy == 'random':
        grpc_server = random_policy()
    elif policy == 'tasks_queue':
        grpc_server = shortest_queue()
    elif policy == 'input_size':
        grpc_server = pick_input(img_shape)
        #如果没找到匹配的大小,暂时先随机
        if grpc_server is None:
            grpc_server = random_policy()
    else:
        grpc_server = lowest_cpu_utilization()
    return grpc_server


if __name__ == '__main__':

    frontend_globals.init()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

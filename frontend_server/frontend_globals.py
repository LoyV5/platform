import multiprocessing
import sys
sys.path.append("../")
from tools.read_config import read_config


def init():
    """Some global variables

    :param grpc_servers: grpc server url list
    :param cpu_usage: cpu_usage list of all servers
    :param memory_usage: memory_usage list of all servers
    :param distribution_function: three distribution functions of selecting a grpc server
    :param tasks_number: processing tasks number of all the grpc servers
    """
    global grpc_servers
    global cpu_usage
    global memory_usage

    #gpu的使用率，各个服务器模型的imgsz
    global gpu_usage
    global imgsz


    grpc_servers = read_config("grpc-url")
    cpu_usage = []
    memory_usage = []
    gpu_usage= []
    imgsz= []


    global distribution_function
    distribution_function = {
        'random': 'random_policy',
        'tasks_queue': 'shortest_queue',
        'cpu_usage': 'lowest_cpu_utilization'
    }

    global tasks_number
    tasks_number = {}
    for grpc_server in grpc_servers:
        tasks_number[grpc_server] = 0



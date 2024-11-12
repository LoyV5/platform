import base64
import json
#from urllib import request, parse
import requests
import time
from loguru import logger


def make_request(url, **msg_dict):
    """Send info to server.

    :param url: server url
    :param msg_dict:
    :return: response object and service delay
    """
    headers = {
        "User-Agent": "Mozilla",
        # 'content-type': 'application/json'
    }

    data = json.dumps(msg_dict)
    t1 = time.time()
    try:
        response = requests.post(url=url,data=data,headers=headers)
        t2 = time.time()
        result = response.text
    except:
        logger.exception("Error request server!")
    else:
        result_dict = json.loads(result)
        try:
            processing_delay = t2 - t1
            arrive_transfer_server_time = (processing_delay - result_dict["process_time"]) / 2
            assert processing_delay != 0
            assert arrive_transfer_server_time != 0
        except AssertionError as err:
            logger.error("processing_delay or arrive_transfer_server_time is 0!")
        else:
            logger.debug("make request well!")
            return result_dict, t1, processing_delay, arrive_transfer_server_time



import json
import requests
import time
from loguru import logger
import edge_globals

def Fpolling(url):
    """
    向forward请求各个cloud的信息
    """
    headers = {
        "User-Agent": "Mozilla",
        # 'content-type': 'application/json'
    }

    t1 = time.time()
    nowtime = time.ctime(t1)
    try:
        response = requests.get(url=url,headers=headers)
        result = response.text
    except:
        logger.exception("Error polling!")
    else:
        result=json.loads(result)
        result['time']=nowtime
        edge_globals.datastore.store_info(result)


        

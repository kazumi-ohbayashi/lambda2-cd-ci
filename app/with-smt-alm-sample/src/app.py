# -*- coding:utf-8 -*-

import os
import logging
import json
import boto3
import requests

logger = logging.getLogger("app")
logger.setLevel(logging.INFO) # DEBUG/INFO/WARNING/ERROR/CRITICAL

NUM_USER_PER_A_WORKER = os.environ.get("NUM_USER_PER_A_WORKER", "5")

# 処理時間計測用
from functools import wraps
import time
def stop_watch(func) :
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        result = func(*args,**kargs)
        elapsed_time =  time.time() - start
        elapsed_time_fmt = "%.6f" % elapsed_time
#        print(f"func {func.__name__} elapsed {elapsed_time_fmt} second")
        logger.debug(f"{func.__name__} elapsed {elapsed_time} second")
        return result
    return wrapper

def get_json(**kwargs):
    params = kwargs.get('params')
    url = kwargs.get('url')
    res_json = {}

    try:
        headers = {'accept':'application/json'}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        status_code = response.status_code
        if (status_code == 200):
            res_json = response.json()
        else:
            # test
            res_json = response.json()
            logger.error("Requests error {}:{}".format(url, response.text))
    except Exception as e:
        logger.error("Requests error {}:{}".format(url, e))

    return res_json

@stop_watch
def do_process(event, context):
#    url = "http://52.196.135.80/"
    url = "http://www.yahoo.co.jp/"
    params = {}
    res = get_json(url=url, params=params)


def lambda_handler(event, context):

    try:
        do_process(event, context)

    except Exception as e:
        logger.exception(e)
        raise e

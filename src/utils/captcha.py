# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Resolve captcha image
import base64
import logging
import time

import requests

logger = logging.getLogger(__name__)


def resolve_captcha_from_bytes(image: bytes):

    img_str = base64.b64encode(image).decode("utf-8")
    API_Key = "23aee2b527d51204ae2d6a75f0191e03"

    # Anti-captcha API structure
    data = {
        "clientKey": API_Key,
        "task": {
            "type": "ImageToTextTask",
            "body": img_str,
            "phrase": False,
            "case": False,
            "numeric": False,
            "math": 0,
            "minLength": 6,
            "maxLength": 6,
        },
    }

    # Create a ImageToTextTask and retrieve taskId from response
    r = requests.post("https://api.anti-captcha.com/createTask", json=data)
    r.raise_for_status()
    task_id = r.json()["taskId"]

    # Polling for task finish.
    ret = ""
    while True:
        data = {"clientKey": API_Key, "taskId": task_id}
        r = requests.post("https://api.anti-captcha.com/getTaskResult", json=data)
        r.raise_for_status()
        if r.json()["status"] == "ready":
            ret = r.json()["solution"]["text"]
            break
        time.sleep(3)
    return ret

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:53 PM
# @Author  : suchang
# @File    : __init__.py.py
import json
from kafka import KafkaConsumer, KafkaProducer
from app.config import Config
from app import app
from flask import current_app


def sub_kafka(topic=''):
    """
    订阅特定topic
    产生特定
    :param topic:
    :return:
    """
    ctx = app.app_context()
    ctx.push()

    def wrapper(func):
        def ex():
            consumer = KafkaConsumer(topic, bootstrap_servers=Config.KAFLKA_HOST,
                                     value_deserializer=lambda v: json.loads(v),
                                     group_id=func.__name__ + '_group'
                                     )
            for msg in consumer:
                current_app.logger.info("received msg : {}".format(msg))
                print("FUNC {} RECEIVED MSG : {}".format(func.__name__, msg))
                func(method=msg.value.get("method"), args=msg.value.get("args"))

        return ex

    return wrapper

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:53 PM
# @Author  : suchang
# @File    : __init__.py.py

import json
from kafka import KafkaProducer
from app import app
from app.utils.logger import log

producer = KafkaProducer(bootstrap_servers=app.config.get("KAFLKA_HOST"), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
topic = app.config.get("KAFLKA_TOPIC")


def send_kafka_message(method, **args):
    producer.send(topic, {
        "method": method,
        "args": args
    })
    log.info("SEND MESSAGE  method : {} args: {}".format(method, str(args)))

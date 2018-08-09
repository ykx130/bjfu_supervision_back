#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 10:27 PM
# @Author  : suchang
# @File    : kafka_consumer.py
import json
from kafka import KafkaConsumer
from app import app
from app.utils.logger import log


topic = app.config.get("KAFLKA_TOPIC")

consumer = KafkaConsumer(bootstrap_servers=app.config.get("KAFLKA_HOST"),
                         value_deserializer=lambda v: json.loads(v))

def run():
    consumer.subscribe([topic])
    for msg in consumer:
        print(msg.value)
        log.info("RECEIVE MESSAGE  method : {} args: {}".format(msg.value["method"], msg.value["args"]))

if __name__ == '__main__':
    run()

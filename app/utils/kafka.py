import json
from kafka import KafkaConsumer, KafkaProducer
from app.config import Config
from flask import current_app


def send_kafka_message(topic, method, **args):
    current_app.kafka_producer.send(topic, value={
        "method": method,
        "args": args
    })
    current_app.logger.info("SEND MESSAGE  method : {} args: {}".format(method, json.dumps(args)))

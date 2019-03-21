import json
from kafka import KafkaConsumer, KafkaProducer
from app.config import Config
from app.utils.logger import log


def sub_kafka(topic=''):
    def wrapper(func):
        def ex():
            consumer = KafkaConsumer(topic, bootstrap_servers=Config.KAFLKA_HOST,
                                     value_deserializer=lambda v: json.loads(v),
                                     group_id=func.__name__ + '_group'
                                     )
            for msg in consumer:
                log.info("received msg : {}".format(msg))
                func(msg.value)

        return ex

    return wrapper


def send_kafka_message(topic, method, **args):
    producer = KafkaProducer(bootstrap_servers=Config.KAFLKA_HOST,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    producer.send(topic, value={
        "method": method,
        "args": args
    })
    log.info("SEND MESSAGE  method : {} args: {}".format(method, json.dumps(args)))

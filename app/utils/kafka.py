import json
from kafka import KafkaConsumer, KafkaProducer
from app.config import Config
from app.utils.logger import log


def send_kafka_message(topic, method, **args):
    producer = KafkaProducer(bootstrap_servers=Config.KAFLKA_HOST,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    producer.send(topic, value={
        "method": method,
        "args": args
    })
    log.info("SEND MESSAGE  method : {} args: {}".format(method, json.dumps(args)))

from app.core.services import lesson_service
from kafka import KafkaConsumer
import json

if __name__ == '__main__':
    lesson_service.change_lesson_status()
    # consumer = KafkaConsumer('form_service', bootstrap_servers=["47.92.110.74:9092", ],
    #                          value_deserializer=lambda v: json.loads(v),
    #                          )
    # for msg in consumer:
    #     print("received msg : {}".format(msg))

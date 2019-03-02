from app.core.services import form_service
from kafka import KafkaConsumer
import json

if __name__ == '__main__':
    form_service.form_service_receiver()
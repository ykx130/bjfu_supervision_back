from flask import Flask, jsonify    
from flask_sqlalchemy import SQLAlchemy
import os
from app.utils.mongodb import mongo
from app.config import config
from flask_login import LoginManager
from app.utils.reids import get_redis_con
from app.utils.mysql import db
from flask_pymongo import PyMongo
import logging
from app.utils.logger import consoleHandler, fileHandler
from kafka import KafkaConsumer, KafkaProducer
import json
from flask_caching import Cache

basedir = os.path.abspath(os.getcwd())

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/401'

cache = Cache(config={'CACHE_TYPE': 'simple'})
redis_cli = get_redis_con(config['default'].REDIS_URL)


def create_app(config_name):
    app = Flask(__name__, static_folder=basedir + '/static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    mongo.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    app.kafka_producer = KafkaProducer(bootstrap_servers=app.config['KAFLKA_HOST'],
                                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    from app.http.handler.form_meta import form_meta_blueprint
    app.register_blueprint(form_meta_blueprint)

    from app.http.handler.form import form_blueprint
    app.register_blueprint(form_blueprint)

    from app.http.handler.event import event_blueprint
    app.register_blueprint(event_blueprint)

    from app.http.handler.lesson import lesson_blueprint
    app.register_blueprint(lesson_blueprint)

    from app.http.handler.activity import activity_blueprint
    app.register_blueprint(activity_blueprint)

    from app.http.handler.user import user_blueprint
    app.register_blueprint(user_blueprint)

    from app.http.handler.consult import consult_blueprint
    app.register_blueprint(consult_blueprint)

    from app.http.handler.notices import notices_blueprint
    app.register_blueprint(notices_blueprint)

    from app.http.handler.notice_lesson import notice_lesson_blueprint
    app.register_blueprint(notice_lesson_blueprint)

    from app.http.handler.lesson_record import lesson_record_blueprint
    app.register_blueprint(lesson_record_blueprint)

    from app.http.handler.model_lesson import model_lesson_blueprint
    app.register_blueprint(model_lesson_blueprint)

    from app.http.handler.other_model_lesson import other_model_lesson_blueprint
    app.register_blueprint(other_model_lesson_blueprint)

    from app.http.handler.page_data import page_data_blueprint
    app.register_blueprint(page_data_blueprint)

    from app.http.handler import captcha_bp
    app.register_blueprint(captcha_bp)
    return app

app = create_app('default')
app.logger.addHandler(consoleHandler)

from app.core.dao.lesson import create_all_lesson_case
#create_all_lesson_case() 

@login_manager.unauthorized_handler
def user_unauthorized_handler():
    return jsonify({
        'msg': '未登录请登陆',
        'code': 401
    }), 401

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.addHandler(fileHandler)
    app.logger.setLevel(gunicorn_logger.level)


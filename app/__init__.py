#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:51 PM
# @Author  : suchang
# @File    : __init__.py.py

from flask import Flask
import os
from app.config import config
from flask_login import LoginManager
from app.utils.reids import get_redis_con
from app.utils.mysql import db

basedir = os.path.abspath(os.path.dirname(__file__))

login_manager = LoginManager()
login_manager.session_protection = 'strong'
redis_cli = get_redis_con(config['default'].REDIS_URL)


def create_app(config_name):
    app = Flask(__name__, static_folder=basedir + '/static')

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from app.http.handler.item_type import item_type_blueprint
    app.register_blueprint(item_type_blueprint)

    from app.http.handler.form_meta import form_meta_blueprint
    app.register_blueprint(form_meta_blueprint)

    from app.http.handler.block_type import block_type_blueprint
    app.register_blueprint(block_type_blueprint)

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

    from app.http.handler.page_data import page_data_blueprint
    app.register_blueprint(page_data_blueprint)

    return app


app = create_app('default')

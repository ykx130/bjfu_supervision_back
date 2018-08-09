#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:51 PM
# @Author  : suchang
# @File    : __init__.py.py

from flask import Flask
import os
from flask_pymongo import PyMongo
from app.config import config


basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name):
    app = Flask(__name__, static_folder=basedir+'/static')

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.http.handler.item_type import item_type_blueprint
    app.register_blueprint(item_type_blueprint)

    from app.http.handler.form_meta import form_meta_blueprint
    app.register_blueprint(form_meta_blueprint)

    from app.http.handler.block_type import block_type_blueprint
    app.register_blueprint(block_type_blueprint)

    from app.http.handler.form import form_blueprint
    app.register_blueprint(form_blueprint)

    from app.http.handler.user import user_blueprint
    app.register_blueprint(user_blueprint)

    from app.http.handler.lesson import lesson_blueprint
    app.register_blueprint(lesson_blueprint)

    return app

app = create_app('default')

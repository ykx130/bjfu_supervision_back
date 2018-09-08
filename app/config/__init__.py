#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:53 PM
# @Author  : suchang
# @File    : __init__.py.py

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    PATIENTS_PRE_PAGE = 20
    MONGO_URI = "mongodb://supervision:root@localhost:27017/supervision"
    MONGO_HOST = "localhost"
    MONGO_USERNAME = 'supervision'
    MONGO_DBNAME = 'supervision'
    MONGO_PASSWORD = 'root'
    #SQLALCHEMY_ECHO = True
    MONGO_PORT = 27017
    MAIL_DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        "mysql+pymysql://root:wshwoaini@localhost:3306/supervision?charset=utf8mb4"
    KAFLKA_HOST = ["47.92.110.74:9091", ]
    KAFLKA_TOPIC = "bjfu_calculate_send_topic"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': Config
}

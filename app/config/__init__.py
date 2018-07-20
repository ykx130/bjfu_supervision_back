#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:53 PM
# @Author  : suchang
# @File    : __init__.py.py

import os
import json
import psutil


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')or 'hard to guess string'
    PATIENTS_PRE_PAGE = 20
    MONGO_URI = 'mongodb://localhost:27017/supervision'
    MONGO_USERNAME = 'myadmin'
    MONGO_PASSWORD = 'secret'
    MONGO_TEST_URI = 'mongodb://localhost:27017/supervision'
    MAIL_DEBUG = True
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
    'default': DevelopmentConfig
}

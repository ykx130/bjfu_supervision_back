#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:54 PM
# @Author  : suchang
# @File    : run.py
#-*- coding=utf-8 -*-

from flask_script import Manager, Shell
from flask import jsonify
from app import create_app
import os
from flask_pymongo import PyMongo

app = create_app('default')
mongo = PyMongo(app)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, mongo=mongo)

manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
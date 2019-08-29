#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:54 PM
# @Author  : suchang
# @File    : run.py
# -*- coding=utf-8 -*-

from flask_script import Manager, Shell
from app import app
from app.utils.mysql import db
from flask_migrate import Migrate, MigrateCommand
from app.utils.mongodb import mongo

manager = Manager(app)
migrate = Migrate(app, db)

from flask import _app_ctx_stack

def create_all():
    db.drop_all()
    db.create_all()


def make_shell_context():
    return dict(app=app, mongo=mongo, db=db, create_all=create_all)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

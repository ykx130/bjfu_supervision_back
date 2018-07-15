#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:52 PM
# @Author  : suchang
# @File    : __init__.py.py

from run import mongo
from flask_pymongo import PyMongo


class FormMeta(object):

    def __init__(self):
        self.model = {
            'meta': {},
            'using': None,
            'items': []
        }
        self.items = list()


    @property
    def using(self):
        return self.model['using']

    @using.setter
    def using(self, using_data):
        self.model['using'] = using_data

    @property
    def meta(self):
        return self.model['meta']

    @meta.setter
    def meta(self, meta_data):
        self.model['meta'].update(meta_data)

    def items_to_dict(self):
        for id, data in enumerate(self.items):
            try:
                data.id = id
                self.model['items'].append(data.model)
            except:
                pass


class Item(object):
    def __init__(self):
        self.model = {
            'id': None,
            'item_name': None,
            'item_type': None,
            'extra': None,
            'payload': {
                'options': []
            }
        }

    @property
    def id(self):
        return self.model['id']

    @id.setter
    def id(self, id_data):
        self.model['id'] = id_data

    @property
    def item_type(self):
        return self.model['item_type']

    @item_type.setter
    def item_type(self, item_type_data):
        self.model['item_type'] = item_type_data

    @property
    def item_name(self):
        return self.model['item_name']

    @item_name.setter
    def item_name(self, item_name_data):
        self.model['item_name'] = item_name_data

    @property
    def extra(self):
        return self.model['extra']

    @extra.setter
    def extra(self, extra_data):
        self.model['extra'] = extra_data


    @property
    def payload(self):
        return self.model['payload']

    @property
    def options(self):
        return self.model['payload']['options']



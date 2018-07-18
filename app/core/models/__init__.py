#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:52 PM
# @Author  : suchang
# @File    : __init__.py.py


class FormMeta(object):

    def __init__(self):
        self.model = {
            'meta': {},
            "identify": None,
            'using': None,
            'items': []
        }
        self.items = list()

    @property
    def identify(self):
        return self.model['identify']

    @identify.setter
    def identify(self, identify_data):
        self.model['identify'] = identify_data

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

    @payload.setter
    def payload(self, payload_data):
        self.model['payload'] = payload_data

    @property
    def options(self):
        return self.model['payload']['options']

    @options.setter
    def options(self, options_data):
        self.model['options'] = options_data


class ItemType(object):

    def __init__(self):
        self.model = {
            'item_type_name':None,
            'item_detail': None,
            'using': True
        }

    @property
    def item_type_name(self):
        return self.model['item_type_name']

    @item_type_name.setter
    def item_type_name(self, item_type_name_data):
        self.model['item_type_name'] = item_type_name_data

    @property
    def item_detail(self):
        return self.model['item_detail']

    @item_detail.setter
    def item_detail(self, item_detail_data):
        self.model['item_detail'] = item_detail_data

    @property
    def using(self):
        return self.model['using']

    @using.setter
    def using(self, using_data):
        self.model['using'] = using_data


class Form(object):
    def __init__(self):
        self.model = {
            "meta_table_id":None,
            "meta":{
                "create_at":None,
                "creator":{}
            },
            "using":True,
            "values":[]
        }

    @property
    def meta_table_id(self):
        return self.model['meta_table_id']

    @meta_table_id.setter
    def meta_table_id(self, meta_table_id_data):
        self.model['meta_table_id'] = meta_table_id_data

    @property
    def values(self):
        return self.model['values']

    @property
    def meta(self):
        return self.model['meta']

    @meta.setter
    def meta(self, meta_data):
        self.model['meta'] = meta_data




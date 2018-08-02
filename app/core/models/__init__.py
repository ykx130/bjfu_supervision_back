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
            'using': True,
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
        for item_id, data in enumerate(self.items):
            try:
                data.item_id = item_id
                self.model['items'].append(data.model)
            except:
                pass


class Item(object):
    def __init__(self):
        self.model = {
            'item_id': None,
            'item_name': None,
            'item_type': None,
            'extra': None,
            'type':None,
            'payload': {
                'options': []
            }
        }

    @property
    def item_id(self):
        return self.model['item_id']

    @item_id.setter
    def item_id(self, id_data):
        self.model['item_id'] = id_data

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


class BlockType(object):

    def __init__(self):
        self.model = {
            'block_type_name':None,
            'block_detail': None,
            'using': True
        }

    @property
    def block_type_name(self):
        return self.model['block_type_name']

    @block_type_name.setter
    def block_type_name(self, block_type_name_data):
        self.model['block_type_name'] = block_type_name_data

    @property
    def block_detail(self):
        return self.model['block_detail']

    @block_detail.setter
    def block_detail(self, block_detail_data):
        self.model['block_detail'] = block_detail_data

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
        self.values = []

    @property
    def meta_table_id(self):
        return self.model['meta_table_id']

    @meta_table_id.setter
    def meta_table_id(self, meta_table_id_data):
        self.model['meta_table_id'] = meta_table_id_data

    @property
    def meta(self):
        return self.model['meta']

    @property
    def using(self):
        return self.model['using']

    @using.setter
    def using(self, using_data):
        self.model['using'] = using_data

    @meta.setter
    def meta(self, meta_data):
        self.model['meta'] = meta_data


    def value_to_dict(self):
        for value in self.values:
            try:
                self.model['values'].append(value.model)
            except:
                pass


class Value(object):
    def __init__(self):
        self.model = {
            'item_id':None,
            'item_type':None,
            'item_name':None,
            'value':None,
        }

    @property
    def item_id(self):
        return self.model['item_id']

    @item_id.setter
    def item_id(self, item_id_data):
        self.model['item_id'] = item_id_data

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
    def value(self):
        return self.model['value']

    @value.setter
    def value(self, value_data):
        self.model['value'] = value_data

class User(object):
    def __init__(self):
        self.model={
            'name': None,
            'information': {
                'birth': None,
                'sex': None
            },
            'events': [],
            'using': True
        }
        self.events= list()

    @property
    def id(self):
        return self.model['id']


    @id.setter
    def id(self, id_data):
        self.model['id'] = id_data

    @property
    def name(self):
        return self.model['name']

    @name.setter
    def name(self, name_data):
        self.model['name'] = name_data

    @property
    def information(self):
        return self.model['information']

    @information.setter
    def information(self, information_data):
        self.model['information'] = information_data

    @property
    def using(self):
        return self.model['using']

    @using.setter
    def using(self, using_data):
        self.model['using'] = using_data

    def items_to_dict(self):
        for id, data in enumerate(self.events):
            try:
                data.event_id = id
                self.model['events'].append(data.model)
            except:
                pass


class Event(object):
    def __init__(self):
        self.model = {
            'event_id': None,
            'time': None,
            'value': None,
            'discripe': None,
            'event_using': True
        }

    @property
    def event_id(self):
        return self.model['event_id']

    @event_id.setter
    def event_id(self, event_id_data):
        self.model['event_id'] = event_id_data

    @property
    def time(self):
        return self.model['time']

    @time.setter
    def time(self, time_data):
        self.model['time'] = time_data

    @property
    def value(self):
        return self.model['value']

    @value.setter
    def value(self, value_data):
        self.model['value'] = value_data

    @property
    def discripe(self):
        return self.model['discripe']

    @discripe.setter
    def discripe(self, discripe_data):
        self.model['discripe'] = discripe_data

    @property
    def using(self):
        return self.model['using']

    @using.setter
    def using(self, using_data):
        self.model['using'] = using_data


class Lesson(object):
    def __init__(self):
        self.model = {
            'lesson_attribute':None,
            'lesson_state':None,
            'lesson_teacher_id':None,
            'lesson_name':None,
            'lesson_teacher_name':None,
            'lesson_semester':None,
            'lesson_level':None,
            'lesson_teacher_unit':None,
            'lesson_unit':None,
            'lesson_year':None,
            'lesson_type':None,
            'lesson_cases':[]
        }
        self.lesson_cases = []

    def lesson_case_to_dict(self):
        for id, data in enumerate(self.lesson_cases):
            try:
                data.id = id
                self.model['lesson_cases'].append(data.model)
            except:
                pass


class LessonCase(object):
    def __init__(self):
        self.model = {
            'id':None,
            'lesson_week':None,
            'lesson_time':None,
            'lesson_class': None,
            'lesson_weekday':None,
            'lesson_room':None,
            'assign_group':None,
            'lesson_attention_reason':None
        }

    @property
    def id(self):
        return self.model['id']

    @id.setter
    def id(self, id_data):
        self.model['id'] = id_data

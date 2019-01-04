from app.utils.mysql import db
from app.utils.url_condition.url_condition_mysql import *


class FormMeta(object):

    def __init__(self):
        self.model = {
            'meta': {'create_by': None},
            'name': None,
            'version': None,
            'using': True,
            'items': []
        }
        self.items = list()

    @property
    def name(self):
        return self.model['name']

    @name.setter
    def name(self, name_data):
        self.model['name'] = name_data

    @property
    def version(self):
        return self.model['version']

    @version.setter
    def version(self, version_data):
        self.model['version'] = version_data

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
        for data in self.items:
            try:
                self.model['items'].append(data.model)
            except:
                pass


class Item(object):
    def __init__(self):
        self.model = {
            'item_name': None,
            'item_type': None,
            'extra': None,
            'type': None,
            'payload': {
                'options': []
            }
        }

    @property
    def type(self):
        return self.model['type']

    @type.setter
    def type(self, type_data):
        self.model['type'] = type_data

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
            'item_type_name': None,
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
            'block_type_name': None,
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
            "bind_meta_id": None,
            "bind_meta_name": None,
            "bind_meta_version": None,
            "meta": {
                "create_at": None,
                "creator": {}
            },
            "status": None,
            "using": True,
            "values": []
        }
        self.values = []

    @property
    def status(self):
        return self.model['status']

    @status.setter
    def status(self, status_data):
        self.model['status'] = status_data

    @property
    def bind_meta_id(self):
        return self.model['bind_meta_id']

    @bind_meta_id.setter
    def bind_meta_id(self, meta_table_id_data):
        self.model['bind_meta_id'] = meta_table_id_data

    @property
    def bind_meta_name(self):
        return self.model['bind_meta_name']

    @bind_meta_name.setter
    def bind_meta_name(self, bind_meta_name_data):
        self.model['bind_meta_name'] = bind_meta_name_data

    @property
    def bind_meta_version(self):
        return self.model['bind_meta_version']

    @bind_meta_version.setter
    def bind_meta_version(self, bind_meta_version_data):
        self.model['bind_meta_version'] = bind_meta_version_data

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
            'item_type': None,
            'item_name': None,
            "type": None,
            'value': None,
            "pyload": dict()
        }

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


class WorkPlan(db.Model):
    __tablename__ = 'work_plans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    term = db.Column(db.String(20))
    form_meta_name = db.Column(db.String(20))
    form_meta_version = db.Column(db.String(20))
    status = db.Column(db.String(20))
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def work_plans(condition: dict):
        url_condition = UrlCondition(condition)
        query = WorkPlan.query.filter(WorkPlan.using == True)
        name_map = {'work_plans': WorkPlan}
        query = process_query(query, url_condition, name_map, WorkPlan)
        return query

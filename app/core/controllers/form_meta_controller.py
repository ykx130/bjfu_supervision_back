from app.core.models import FormMeta, Item
from flask_pymongo import ObjectId
import json

def find_form_meta(mongo, _id):
    try:
        condition = {'using':True, '_id':ObjectId(_id)}
    except:
        return None
    data = mongo.db.form_meta.find_one(condition)
    return data

def find_form_metas(mongo, condition=None):
    condition['using'] = True
    if condition is None:
        return mongo.db.form_meta.find()
    if '_id' in condition:
        try:
            condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
        except:
            return None
    datas = mongo.db.form_meta.find(condition)
    return datas

# 传入字典型返回筛选过的数据的cursor, 遍历cursor得到的是字典


def insert_form_meta(mongo, form_meta):
    form_meta.items_to_dict()
    mongo.db.form_meta.insert(form_meta.model)

# 传入一个FormMeta对象，存入数据库


def delete_form_meta(mongo, condition=None):
    condition['using'] = True
    if condition is None:
        return False
    try:
        mongo.db.form_meta.update(condition, {"$set":{"using":False}})
    except:
        return False
    return True
# 传入一个用于匹配的字典，更改匹配到的所有文档的using值


def request_to_class(json_request):
    form_meta = FormMeta()
    identify = json_request.get('identify', None)
    meta = json_request.get('meta', {})
    item_datas = json_request.get('items', {})
    form_meta.identify = identify
    if meta is not None:
        form_meta.meta = meta
    if item_datas is not None:
        for item_data in item_datas:
            item = Item()
            for k, v in item_data.items():
                if k in item.model:
                    item.model[k]= v
            form_meta.items.append(item)
    return form_meta
# 传入request.json字典,返回一个FormMeta对象


def to_json_list(form_meta):
    _id = form_meta.get('_id', None)
    meta = form_meta.get('meta', {})
    identify = form_meta.get('identify', None)
    using = form_meta.get('using', None)
    json_list = {
        '_id': _id,
        'meta': meta,
        'identify': identify
    }
    return json_list


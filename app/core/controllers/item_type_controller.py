from app.core.models.form import ItemType
from flask_pymongo import ObjectId
import json


def insert_item_type(mongo, item_type):
    mongo.db.item_type.insert(item_type.model)
    return True
#传入ItemType对象，存入数据库

def find_item_type(mongo, _id):
    condition = {'using': True, '_id': ObjectId(_id)}
    data = mongo.db.item_type.find_one(condition)
    return data

def find_item_types(mongo, condition=None):
    condition['using'] = True
    if condition is None:
        return mongo.db.item_type.find()
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    datas = mongo.db.item_type.find(condition)
    return datas

#传入一个判断的字典，返回查询数据的cursor


def delete_item_type(mongo, condition=None):
    condition['using'] = True
    if condition is None:
        return False
    mongo.db.item_type.update(condition, {"$set": {"using": False}})
    return True


def update_item_type(mongo, condition=None, update_dict= None):
    condition['using'] = True
    if condition is None:
        condition = {}
    mongo.db.item_type.update(condition, {"$set": update_dict})
    return True

#传入一个判断字典，将using字段值更改


def request_to_class(json_request={}):
    item_type = ItemType()
    for k, v in json_request.items():
            item_type.model[k]= v
    return item_type

#传入request.json字典,返回一个ItemType对象


def request_to_change(json_request={}):
    change = {}
    for k, v in json_request.items():
            change[k] = v
    return change






#将不可序列化的对象可序列化


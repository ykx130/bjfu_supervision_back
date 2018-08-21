from app.core.models.form import ItemType
from flask_pymongo import ObjectId


def insert_item_type(mongo, item_type):
    try:
        mongo.db.item_type.insert(item_type.model)
    except Exception as e:
        return False, e
    return True, None
# 传入ItemType对象，存入数据库


def find_item_type(mongo, _id):
    try:
        condition = {'using': True, '_id': ObjectId(_id)}
        data = mongo.db.item_type.find_one(condition)
    except Exception as e:
        return None, e
    return data, None


def find_item_types(mongo, condition=None):
    if condition is None:
        condition['using'] = True
        return mongo.db.item_type.find(condition), None
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    try:
        datas = mongo.db.item_type.find(condition)
    except Exception as e:
        return None, e
    return datas, None

# 传入一个判断的字典，返回查询数据的cursor


def delete_item_type(mongo, condition=None):
    if condition is None:
        return False, None
    condition['using'] = True
    try:
        mongo.db.item_type.update(condition, {"$set": {"using": False}})
    except Exception as e:
        return None, e
    return True, None


def update_item_type(mongo, condition=None, update_dict= None):
    if condition is None:
        condition = dict()
        condition['using'] = True
    try:
        mongo.db.item_type.update(condition, {"$set": update_dict})
    except Exception as e:
        return None, e
    return True, None

# 传入一个判断字典，将using字段值更改


def request_to_class(json_request=None):
    item_type = ItemType()
    for k, v in json_request.items():
            item_type.model[k]= v
    return item_type

# 传入request.json字典,返回一个ItemType对象


def request_to_change(json_request=None):
    change = {}
    for k, v in json_request.items():
            change[k] = v
    return change




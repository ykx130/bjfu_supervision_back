from app.core.models.form import BlockType
from flask_pymongo import ObjectId


def insert_block_type(block_type):
    from app.utils.mongodb import mongo
    try:
        mongo.db.block_type.insert(block_type.model)
    except Exception as e:
        return False, e
    return True, None


# 传入BlockType对象，存入数据库


def find_block_type(_id):
    from app.utils.mongodb import mongo
    try:
        condition = {'using': True, '_id': ObjectId(_id)}
        data = mongo.db.block_type.find_one(condition)
    except Exception as e:
        return None, e
    return data, None


def find_block_types(condition=None):
    from app.utils.mongodb import mongo
    if condition is None:
        condition['using'] = True
        return mongo.db.block_type.find(), None
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    try:
        datas = mongo.db.block_type.find(condition)
    except Exception as e:
        return None, e
    return datas, None


# 传入一个判断的字典，返回查询数据的cursor


def delete_block_type(condition=None):
    from app.utils.mongodb import mongo
    if condition is None:
        return False, None
    condition['using'] = True
    try:
        mongo.db.block_type.update(condition, {"$set": {"using": False}})
    except Exception as e:
        return False, e
    return True, None


def update_block_type(condition=None, update_dict=None):
    from app.utils.mongodb import mongo
    if condition is None:
        condition = dict()
        condition['using'] = True
    try:
        mongo.db.block_type.update(condition, {"$set": update_dict})
    except Exception as e:
        return False, e
    return True, None


# 传入一个判断字典，将using字段值更改


def request_to_class(json_request=None):
    block_type = BlockType()
    for k, v in json_request.items():
        block_type.model[k] = v
    return block_type


# 传入request.json字典,返回一个BlockType对象


def request_to_change(json_request=None):
    change = {}
    for k, v in json_request.items():
        change[k] = v
    return change

# 将不可序列化的对象可序列化

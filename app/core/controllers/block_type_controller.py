from app.core.models.form import BlockType
from flask_pymongo import ObjectId
import json


def insert_block_type(mongo, block_type):
    mongo.db.block_type.insert(block_type.model)
#传入BlockType对象，存入数据库

def find_block_type(mongo, _id):
    condition = {'using': True, '_id': ObjectId(_id)}
    data = mongo.db.block_type.find_one(condition)
    return data

def find_block_types(mongo, condition=None):
    condition['using'] = True
    if condition is None:
        return mongo.db.block_type.find()
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    datas = mongo.db.block_type.find(condition)
    return datas

#传入一个判断的字典，返回查询数据的cursor


def delete_block_type(mongo, condition=None):
    condition['using'] = True
    if condition is None:
        return False
    mongo.db.block_type.update(condition, {"$set": {"using": False}})
    return True


def update_block_type(mongo, condition=None, update_dict= None):
    condition['using'] = True
    if condition is None:
        condition = {}
    mongo.db.block_type.update(condition, {"$set": update_dict})


#传入一个判断字典，将using字段值更改


def request_to_class(json_request={}):
    block_type = BlockType()
    for k, v in json_request.items():
        block_type.model[k]= v
    return block_type

#传入request.json字典,返回一个BlockType对象


def request_to_change(json_request={}):
    change = {}
    for k, v in json_request.items():
            change[k] = v
    return change






#将不可序列化的对象可序列化


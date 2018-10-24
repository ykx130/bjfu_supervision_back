from app.core.models.form import ItemType
from app.utils.url_condition.url_condition_mongodb import *
from app.utils.Error import CustomError


def insert_item_type(item_type):
    from app.utils.mongodb import mongo
    try:
        mongo.db.item_type.insert(item_type.model)
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    return True, None


# 传入ItemType对象，存入数据库


def find_item_type(_id):
    from app.utils.mongodb import mongo
    try:
        condition = {'using': True, '_id': ObjectId(_id)}
        data = mongo.db.item_type.find_one(condition)
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if data is None:
        return None, CustomError(404, 404, 'item type not found')
    return data, None


def find_item_types(condition=None):
    from app.utils.mongodb import mongo
    url_condition = UrlCondition(condition)
    if url_condition.filter_dict is None:
        datas = mongo.db.form_meta.find()
        return datas, datas.count(), None
    if '_id' in url_condition.filter_dict:
        url_condition.filter_dict['_id']['$in'] = [ObjectId(item) for item in url_condition.filter_dict['_id']['$in']]
    try:
        datas = mongo.db.item_type.find(url_condition.filter_dict)
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    datas = sort_limit(datas, url_condition.sort_limit_dict)
    paginate = Paginate(datas, url_condition.page_dict)
    datas = paginate.data_page
    return datas, paginate.total, None


# 传入一个判断的字典，返回查询数据的cursor


def delete_item_type(condition=None):
    from app.utils.mongodb import mongo
    if condition is None:
        return False, None
    condition['using'] = True
    try:
        mongo.db.item_type.update(condition, {"$set": {"using": False}})
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return True, None


def update_item_type(condition=None, update_dict=None):
    from app.utils.mongodb import mongo
    if condition is None:
        condition = dict()
        condition['using'] = True
    try:
        mongo.db.item_type.update(condition, {"$set": update_dict})
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return True, None


# 传入一个判断字典，将using字段值更改


def request_to_class(json_request=None):
    item_type = ItemType()
    for k, v in json_request.items():
        item_type.model[k] = v
    return item_type


# 传入request.json字典,返回一个ItemType对象


def request_to_change(json_request=None):
    change = {}
    for k, v in json_request.items():
        change[k] = v
    return change

from app.core.services import item_type_service


def insert_item_type(mongo, item_type):
    (ifSuccess, err) = item_type_service.insert_item_type(mongo, item_type)
    return ifSuccess, err


# 传入ItemType对象，存入数据库


def find_item_type(mongo, _id):
    (item_type, err) = item_type_service.find_item_type(mongo, _id)
    return item_type, err


def find_item_types(mongo, condition=None):
    (item_types, err) = item_type_service.find_item_types(mongo, condition)
    return item_types, err


# 传入一个判断的字典，返回查询数据的cursor


def delete_item_type(mongo, condition=None):
    (ifSuccess, err) = item_type_service.delete_item_type(mongo, condition)
    return ifSuccess, err


def update_item_type(mongo, condition=None, update_dict=None):
    (ifSuccess, err) = item_type_service.update_item_type(mongo, condition, update_dict)
    return ifSuccess, err


# 传入一个判断字典，将using字段值更改


def request_to_class(json_request=None):
    return item_type_service.request_to_class(json_request)


# 传入request.json字典,返回一个ItemType对象


def request_to_change(json_request=None):
    return item_type_service.request_to_change(json_request)

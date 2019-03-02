from app.core.services import item_type_service
from app.utils.url_condition.url_args_to_dict import args_to_dict


def insert_item_type(request_json):
    item_type = item_type_service.request_to_class(request_json)
    (ifSuccess, err) = item_type_service.insert_item_type(item_type)
    if err is not None:
        return False, err
    return ifSuccess, None


# 传入ItemType对象，存入数据库


def find_item_type(_id):
    (item_type, err) = item_type_service.find_item_type(_id)
    if err is not None:
        return None, err
    item_type_model = item_type_service.object_to_str(item_type)
    return item_type_model, None


def find_item_types(condition=None):
    condition_fin = args_to_dict(condition)
    (item_types, num, err) = item_type_service.find_item_types(condition_fin)
    if err is not None:
        return None, None, err
    item_types_model = [item_type_service.object_to_str(item_type) for item_type in item_types]
    return item_types_model, num, None


# 传入一个判断的字典，返回查询数据的cursor


def delete_item_type(condition=None):
    (ifSuccess, err) = item_type_service.delete_item_type(condition)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_item_type(condition=None, request_json=None):
    change = item_type_service.request_to_change(request_json)
    (ifSuccess, err) = item_type_service.update_item_type(condition, change)
    if err is not None:
        return False, err
    return ifSuccess, None

# 传入一个判断字典，将using字段值更改


# 传入request.json字典,返回一个ItemType对象

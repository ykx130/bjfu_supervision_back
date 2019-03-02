from app.core.services import block_type_service
from app.utils.url_condition.url_condition_mongodb import *
from app.utils.url_condition.url_args_to_dict import args_to_dict


def insert_block_type(request_json):
    block_type = block_type_service.request_to_class(request_json)
    (ifSuccess, err) = block_type_service.insert_block_type(block_type)
    if err is not None:
        return False, err
    return ifSuccess, None


# 传入BlockType对象，存入数据库


def find_block_type(_id):
    (block_type, err) = block_type_service.find_block_type(_id)
    if err is not None:
        return None, err
    block_type_model = object_to_str(block_type)
    return block_type_model, None


def find_block_types(condition=None):
    condition_fin = args_to_dict(condition)
    url_condition = UrlCondition(condition_fin)
    (block_types, err) = block_type_service.find_block_types(url_condition.filter_dict)
    if err is not None:
        return None, None, err
    block_types = sort_limit(block_types, url_condition.sort_limit_dict)
    paginate = Paginate(block_types, url_condition.page_dict)
    block_types_model = [object_to_str(block_type) for block_type in block_types]
    return block_types_model, paginate.total, None


# 传入一个判断的字典，返回查询数据的cursor


def delete_block_type(condition=None):
    (ifSuccess, err) = block_type_service.delete_block_type(condition)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_block_type(condition=None, request_json=None):
    change = block_type_service.request_to_change(request_json)
    (ifSuccess, err) = block_type_service.update_block_type(condition, change)
    if err is not None:
        return False, err
    return ifSuccess, None

# 传入一个判断字典，将using字段值更改

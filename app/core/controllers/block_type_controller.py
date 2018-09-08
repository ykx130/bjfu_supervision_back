from app.core.services import block_type_service


def insert_block_type(mongo, block_type):
    (ifSuccess, err) = block_type_service.insert_block_type(mongo, block_type)
    return ifSuccess, err


# 传入BlockType对象，存入数据库


def find_block_type(mongo, _id):
    (block_type, err) = block_type_service.find_block_type(mongo, _id)
    return block_type, err


def find_block_types(mongo, condition=None):
    (block_types, err) = block_type_service.find_block_types(mongo, condition)
    return block_types, err


# 传入一个判断的字典，返回查询数据的cursor


def delete_block_type(mongo, condition=None):
    (ifSuccess, err) = block_type_service.delete_block_type(mongo, condition)
    return ifSuccess, err


def update_block_type(mongo, condition=None, update_dict=None):
    (ifSuccess, err) = block_type_service.update_block_type(mongo, condition, update_dict)
    return ifSuccess, err


# 传入一个判断字典，将using字段值更改


def request_to_class(json_request=None):
    return block_type_service.request_to_class(json_request)


# 传入request.json字典,返回一个BlockType对象


def request_to_change(json_request=None):
    return block_type_service.request_to_change(json_request)

# 将不可序列化的对象可序列化

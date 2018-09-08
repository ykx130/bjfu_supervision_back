from app.core.services import form_meta_service


def find_form_meta(mongo, name, version=None):
    (form_meta, err) = form_meta_service.find_form_meta(mongo, name, version)
    return form_meta, err


def find_form_metas(mongo, condition=None):
    (form_metas, err) = form_meta_service.find_form_metas(mongo, condition)
    return form_metas, err


# 传入字典型返回筛选过的数据的cursor, 遍历cursor得到的是字典


def insert_form_meta(mongo, form_meta):
    (ifSuccess, err) = form_meta_service.insert_form_meta(mongo, form_meta)
    return ifSuccess, err


# 传入一个FormMeta对象，存入数据库


def delete_form_meta(mongo, condition=None):
    (ifSuccess, err) = form_meta_service.delete_form_meta(mongo, condition)
    return ifSuccess, err


# 传入一个用于匹配的字典，更改匹配到的所有文档的using值


def request_to_class(json_request):
    return form_meta_service.request_to_class(json_request)


# 传入request.json字典,返回一个FormMeta对象


def to_json_list(form_meta):
    return form_meta_service.to_json_list(form_meta)

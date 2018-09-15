from app.core.services import form_meta_service


def find_form_meta(name, version=None):
    (form_meta, err) = form_meta_service.find_form_meta(name, version)
    if err is not None:
        return None, err
    if form_meta is None:
        return None, None
    form_meta_model = form_meta_service.object_to_str(form_meta)
    return form_meta_model, err


def find_form_metas(condition=None):
    (form_metas, total, err) = form_meta_service.find_form_metas(condition)
    form_metas_list = [form_meta_service.to_json_list(form_meta) for form_meta in form_metas]
    form_metas_model = [form_meta_service.object_to_str(form_meta) for form_meta in form_metas_list]
    return form_metas_model, total, err


# 传入字典型返回筛选过的数据的cursor, 遍历cursor得到的是字典


def insert_form_meta(request_json):
    form_meta = form_meta_service.request_to_class(request_json)
    (ifSuccess, err) = form_meta_service.insert_form_meta(form_meta)
    return ifSuccess, err


# 传入一个FormMeta对象，存入数据库


def delete_form_meta(condition=None):
    (ifSuccess, err) = form_meta_service.delete_form_meta(condition)
    return ifSuccess, err


from app.core.services import form_meta_service


def find_form_meta(name, version=None):
    (form_meta, err) = form_meta_service.find_form_meta(name, version)
    if err is not None:
        return None, err
    form_meta_model = form_meta_service.object_to_str(form_meta)
    return form_meta_model, None


def find_history_form_meta(name, condition):
    condition_fin = dict()
    if condition is None:
        condition_fin['name'] = [name]
    else:
        for key in condition:
            for value in condition.getlist(key):
                if key not in condition_fin:
                    condition_fin[key] = [value]
                else:
                    condition_fin[key].append(value)
    (form_metas, total, err) = form_meta_service.find_form_metas(condition)
    if err is not None:
        return None, None, err
    form_metas_models = list()
    for form_meta in form_metas:
        (form_meta_model, err) = form_meta_service.to_json_dict(form_meta)
        if err is not None:
            return None, None, err
        form_metas_models.append(form_meta_model)
    return form_metas_models, total, None


def find_form_metas(condition=None):
    condition_fin = dict()
    if condition is None:
        condition_fin['using'] = [True]
    else:
        for key in condition:
            for value in condition.getlist(key):
                if key not in condition_fin:
                    condition_fin[key] = [value]
                else:
                    condition_fin[key].append(value)
        condition_fin['using'] = [True]
    (form_metas, total, err) = form_meta_service.find_form_metas(condition_fin)
    if err is not None:
        return None, None, err
    form_metas_models = list()
    for form_meta in form_metas:
        (form_meta_model, err) = form_meta_service.to_json_dict(form_meta)
        if err is not None:
            return None, None, err
        form_metas_models.append(form_meta_model)
    return form_metas_models, total, None


def find_form_meta_history(condition):
    (form_metas, num, err) = form_meta_service.find_form_metas(condition)
    if err is not None:
        return None, None, err
    form_metas_models = list()
    for form_meta in form_metas:
        (form_meta_model, err) = form_meta_service.to_json_dict(form_meta)
        if err is not None:
            return None, None, err
        form_metas_models.append(form_meta_model)
    return form_metas_models, num, None


# 传入字典型返回筛选过的数据的cursor, 遍历cursor得到的是字典


def insert_form_meta(request_json):
    form_meta = form_meta_service.request_to_class(request_json)
    (ifSuccess, err) = form_meta_service.insert_form_meta(form_meta)
    if err is not None:
        return False, err
    return ifSuccess, None


# 传入一个FormMeta对象，存入数据库


def delete_form_meta(condition=None):
    (ifSuccess, err) = form_meta_service.delete_form_meta(condition)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_form_meta(name, request_json=None):
    (form_meta, err) = form_meta_service.find_form_meta(name)
    if err is not None:
        return False, err
    (ifSuccess, err) = form_meta_service.delete_form_meta({'name': name, 'version': form_meta['version']})
    if err is not None:
        return False, err
    form_meta = form_meta_service.request_to_class(request_json)
    (ifSuccess, err) = form_meta_service.insert_form_meta(form_meta)
    if err is not None:
        return False, err
    return ifSuccess, None

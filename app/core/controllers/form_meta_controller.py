from app.core.services import form_meta_service
from app.utils.Error import CustomError
from app.utils.url_condition.url_args_to_dict import args_to_dict


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
        condition_fin = args_to_dict(condition)
        condition_fin['name'] = [name]
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


def find_form_metas(condition=None):
    condition_fin = dict()
    if condition is None:
        condition_fin['using'] = [True]
    else:
        condition_fin = args_to_dict(condition)
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
    condition_fin = args_to_dict(condition)
    (form_metas, num, err) = form_meta_service.find_form_metas(condition_fin)
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


def find_work_plan(id):
    (work_plan, err) = form_meta_service.find_work_plan(id)
    if err is not None:
        return None, err
    (work_plan_model, err) = form_meta_service.work_plan_to_dict(work_plan)
    if err is not None:
        return None, err
    return work_plan_model, None


def find_work_plans(condition):
    condition_fin = args_to_dict(condition)
    (work_plans, num, err) = form_meta_service.find_work_plans(condition_fin)
    if err is not None:
        return None, None, err
    work_plans_model = list()
    for work_plan in work_plans:
        (work_plan_model, err) = form_meta_service.work_plan_to_dict(work_plan)
        if err is not None:
            return None, None, err
        work_plans_model.append(work_plan_model)
    return work_plans_model, num, None


def insert_work_plan(request_json):
    form_meta_name = request_json['form_meta_name'] if 'form_meta_name' in request_json else None
    if form_meta_name is None:
        return False, CustomError(500, 200, 'form_meta_name must be given')
    form_meta_version = request_json['form_meta_version'] if 'form_meta_version' in request_json else None
    if form_meta_version is None:
        return False, CustomError(500, 200, 'form_meta_version must be given')
    condition = {'form_meta_name': [form_meta_name], 'form_meta_version': [form_meta_version], 'using': [True]}
    (form_meta, num, err) = form_meta_service.find_form_metas(condition)
    if num == 0:
        return False, CustomError(404, 404, 'form_meta not found')
    (ifSuccess, err) = form_meta_service.insert_work_plan(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_work_plan(id, request_json):
    (ifSuccess, err) = form_meta_service.update_work_plan(id, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def delete_work_plan(id):
    (ifSuccess, err) = form_meta_service.delete_work_plan(id)
    if err is not None:
        return False, err
    return True, None

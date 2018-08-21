from flask_pymongo import ObjectId
from app.core.models.form import Form, Value


def find_forms(mongo, condition=None):
    if condition is None:
        condition['using'] = True
        return mongo.db.form.find(condition), None
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    try:
        datas = mongo.db.form.find(condition)
    except Exception as e:
        return None, e
    return datas, None


def find_form(mongo, _id):
    condition = {'using': True, '_id': ObjectId(_id)}
    try:
        data = mongo.db.form.find_one(condition)
    except Exception as e:
        return None, e
    return data, None


def insert_form(mongo, form):
    form.value_to_dict()
    try:
        mongo.db.form.insert(form.model)
    except Exception as e:
        return False, e
    return True, None


def delete_form(mongo, condition=None):
    if condition is None:
        return False, None
    try:
        mongo.db.form.update(condition, {"$set": {"using": False}})
    except Exception as e:
        return False, e
    return True, None


def update_form(mongo, condition=None, change_item=None):
    if condition is None:
        condition = dict()
        condition['using'] = True
    try:
        mongo.db.form.update(condition, {"$set": change_item})
    except Exception as e:
        return False, e
    return True, None


def to_json_list(form):
    _id = form.get('_id', None)
    meta = form.get('meta', {})
    bind_meta_id = form.get('bind_meta_id', None)
    bind_meta_name = form.get('bind_meta_name', None)
    bind_meta_version = form.get('bind_meta_version', None)
    json_list = {
        '_id': _id,
        'meta': meta,
        'bind_meta_id': bind_meta_id,
        'bind_meta_name': bind_meta_name,
        'bind_meta_version': bind_meta_version
    }
    return json_list


def request_to_class(json_request):
    form = Form()
    bind_meta_id = json_request.get('bind_meta_id', None)
    bind_meta_name = json_request.get('bind_meta_name', None)
    bind_meta_version = json_request.get('bind_meta_version', None)
    meta = json_request.get('meta', {})
    values = json_request.get('values', [])
    using = json_request.get('using', True)
    form.using = using
    form.bind_meta_id = bind_meta_id
    form.bind_meta_name = bind_meta_name
    form.bind_meta_version = bind_meta_version
    form.meta = meta
    for value_item in values:
        value = Value()
        for k, v in value_item.items():
            value.model[k] = v
        form.values.append(value)
    return form

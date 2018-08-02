from flask_pymongo import ObjectId
from app.core.models import Form, Value


def find_forms(mongo, condition=None):
    condition['using'] = True
    if condition is None:
        return mongo.db.form.find()
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    datas = mongo.db.form.find(condition)
    return datas


def find_form(mongo, _id):
    try:
        condition = {'using':True, '_id':ObjectId(_id)}
    except:
        return None
    data = mongo.db.form.find_one(condition)
    return data


def insert_form(mongo, form):
    form.value_to_dict()
    mongo.db.form.insert(form.model)


def delete_form(mongo, condition=None):
    if condition is None:
        return False
    try:
        mongo.db.form.update(condition, {"$set":{"using":False}})
    except:
        return False
    return True


def update_form(mongo, condition=None, change_item = None):
    if condition is None:
        return False
    try:
        mongo.db.form.update(condition, {"$set":change_item})
    except:
        return False
    return True


def to_json_list(form):
    _id = form.get('_id', None)
    meta = form.get('meta', {})
    meta_table_id = form.get('meta_table_id', None)
    json_list = {
        '_id':_id,
        'meta':meta,
        'meta_table_id':meta_table_id
    }
    return json_list


def request_to_class(json_request):
    form = Form()
    meta_table_id = json_request.get('meta_table_id', None)
    meta = json_request.get('meta', {})
    values = json_request.get('values', {})
    using = json_request.get('using', True)
    form.using = using
    form.meta_table_id = meta_table_id
    if meta is not None:
        form.meta = meta
    if values is not None:
        for value_item in values:
            value = Value()
            for k, v in value_item.items():
                value.model[k] = v
            form.values.append(value)
    return form

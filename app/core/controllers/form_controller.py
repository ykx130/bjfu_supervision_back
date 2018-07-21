from flask_pymongo import ObjectId
from app.core.models import Form,Item,Value


def find_form(mongo, condition=None):
    if condition is None:
        return mongo.db.form.find()
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    datas = mongo.db.form_meta.find(condition)
    return datas


def insert_form(mongo, form):
    mongo.db.form.insert(form.model)


def delete_form(mongo,condition=None):
    if condition is None:
        return False
    try:
        mongo.db.form.update(condition,{"$set":{"using":False}})
    except:
        return False
    return True


def request_to_class(json_request):
    form=Form()
    meta_table_id=json_request.get('meta_table_id',None)
    meta=json_request.get('meta',{})
    value_datas=json_request.get('values',[])
    form.meta_table_id=meta_table_id
    if meta is not None:
        form.meta=meta
    if value_datas is not None:
        for value_data in value_datas:
            value=Value()
            for k,v in value_data.values():
                if k in value.model:
                    value.model[k]=v
            form.values.append(value)
    return form


def to_json_list(form):
    _id = form.get('_id', None)
    meta = form.get('meta', {})
    meta_table_id = form.get('meta_table_id', None)
    using = form.get('using', None)
    json_list = {
        '_id': _id,
        'meta': meta,
        'meta_table_id': meta_table_id,
        'using': using
    }
    return json_list

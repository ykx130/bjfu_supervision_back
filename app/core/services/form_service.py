from flask_login import current_user
from datetime import datetime
from app.core.models.form import Form, Value
from app.utils.url_condition.url_condition_mongodb import *
from app.utils.Error import CustomError



def find_forms(condition=None):
    from app.utils.mongodb import mongo
    url_condition = UrlCondition(condition)
    if url_condition.filter_dict is None:
        datas = mongo.db.form.find()
        return datas, datas.count(), None
    if '_id' in url_condition.filter_dict:
        url_condition.filter_dict['_id']['$in'] = [ObjectId(item) for item in url_condition.filter_dict['_id']['$in']]
    try:
        datas = mongo.db.form.find(url_condition.filter_dict)
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    datas = sort_limit(datas, url_condition.sort_limit_dict)
    paginate = Paginate(datas, url_condition.page_dict)
    datas = paginate.data_page
    return datas, paginate.total, None


def find_form(_id):
    from app.utils.mongodb import mongo
    if _id is None:
        return None, CustomError(500, 500, '_id must be given')
    condition = {'using': True, '_id': ObjectId(_id)}
    try:
        data = mongo.db.form.find_one(condition)
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if data is None:
        return None, CustomError(404, 404, 'form not found')
    return data, None


def insert_form(form):
    from app.utils.mongodb import mongo
    form.value_to_dict()
    try:
        mongo.db.form.insert(form.model)
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_form(condition=None):
    from app.utils.mongodb import mongo
    if condition is None:
        return False, CustomError(500, 500, 'condition can not be None')
    try:
        mongo.db.form.update(condition, {"$set": {"using": False}})
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    return True, None


def update_form(condition=None, change_item=None):
    from app.utils.mongodb import mongo
    if condition is None:
        condition = dict()
        condition['using'] = True
    try:
        mongo.db.form.update(condition, {"$set": change_item})
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    return True, None


def to_json_dict(form):
    try:
        json_dict = {
            '_id': str(form.get('_id', None)),
            'meta': form.get('meta', {}),
            'bind_meta_id': form.get('bind_meta_id', None),
            'bind_meta_name': form.get('bind_meta_name', None),
            'bind_meta_version': form.get('bind_meta_version', None)
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return json_dict, None



def request_to_class(json_request):
    form = Form()
    bind_meta_id = json_request.get('bind_meta_id', None)
    bind_meta_name = json_request.get('bind_meta_name', None)
    bind_meta_version = json_request.get('bind_meta_version', None)
    meta = json_request.get('meta', {"created_by": current_user.username,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
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

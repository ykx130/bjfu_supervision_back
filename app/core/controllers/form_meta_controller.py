from app.core.models import FormMeta, Item
import json


def find_form_meta(mongo, condition= None):
    if condition is None:
        return mongo.db.form_meta.find()
    datas = mongo.db.form_meta.find(condition)
    return datas

#传入字典型返回筛选过的数据的cursor, 遍历cursor得到的是字典


def insert_form_meta(mongo, form_meta):
    form_meta.items_to_dict()
    mongo.db.form_meta.insert(form_meta.model)

#传入一个FormMeta对象，存入数据库


def delete_form_meta(mongo, condition= None):
    if condition is None:
        return False
    try:
        mongo.db.form_meta.update(condition, {"$set":{"using":False}})
    except:
        return False
    return True

#传入一个用于匹配的字典，更改匹配到的所有文档的using值


def request_to_class(json_request):
    form_meta = FormMeta()

    meta = json_request.get('meta', {})
    item_datas = json_request.get('items', {})
    if meta is not None:
        form_meta.meta = meta
    if item_datas is not None:
        for item_data in item_datas:
            item = Item()
            for k, v in item_data.items():
                if k in item.model:
                    item.model[k]= v
            form_meta.items.append(item)
    return form_meta

#传入request.json字典,返回一个FormMeta对象

def dict_serializable(dict_unserializalbe):
    r = {}
    for k, v in dict_unserializalbe.items():
        try:
            r[k] = json.loads(v)
        except:
            r[k] = str(v)
    return r

#将不可序列化的对象可序列化


def to_json_list(form_meta):
    _id = form_meta.get('_id', None)
    meta = form_meta.get('meta', {})
    using = form_meta.get('using', None)
    json_list = {
        '_id':_id,
        'meta':meta,
        'using':using
    }
    return json_list


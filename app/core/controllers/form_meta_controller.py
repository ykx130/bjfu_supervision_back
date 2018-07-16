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


def delete_form_meta(mongo, condition= None):
    if condition is None:
        return False
    mongo.db.form_meta.update(condition, {"$set":{"using":False}})


def request_to_class(json_request):
    form_meta = FormMeta()

    meta = json_request.get('meta', {})
    item_datas = json_request.get('items', {})
    if meta is not None:
        form_meta.meta = meta
    if item_datas is not None:
        for item_data in item_datas:
            item = Item()
            item.model = item_data
            form_meta.items.append(item)
    return form_meta


def dict_serializable(dict_unserializalbe):
    r = {}
    for k, v in dict_unserializalbe.items():
        try:
            r[k] = json.loads(v)
        except:
            r[k] = str(v)
    return r


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

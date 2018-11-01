import json
import jieba
from collections import Counter
from flask_login import current_user
from datetime import datetime
from app.core.models.form import Form, Value
from app.core.services import lesson_record_service
from app.utils.url_condition.url_condition_mongodb import *
from app.utils.Error import CustomError
from app.streaming import sub_kafka
from app import redis_cli


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
            'status': form.get('status'),
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
    meta = json_request.get('meta', {})
    meta.update({"created_by": current_user.username,
                 "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    status = json_request.get("status", '待提交')
    values = json_request.get('values', [])
    using = json_request.get('using', True)
    form.using = using
    form.bind_meta_id = bind_meta_id
    form.bind_meta_name = bind_meta_name
    form.bind_meta_version = bind_meta_version
    form.meta = meta
    form.status = status
    for value_item in values:
        value = Value()
        for k, v in value_item.items():
            value.model[k] = v
        form.values.append(value)
    return form


def calculate_map(meta_name):
    item_map = {}
    word_cloud = {}
    from app.utils.mongodb import mongo
    forms = mongo.db.form.find({"bind_meta_name": meta_name})

    for form in forms:
        for v in form.get("values"):
            if v.get('item_type') == "radio_option":
                # 处理单选
                if not item_map.get(v['item_name']):
                    # 初始化
                    point = {o['value']: {"option": o, "num": 0} for o in v.get("payload", {}).get("options", [])}
                    point[v['value']]['num'] = point[v['value']]['num'] + 1
                    item_map[v['item_name']] = {
                        "item_name": v['item_name'],
                        "point": list(point.values())
                    }
                else:
                    # 存在直接+1
                    point = item_map[v['item_name']]["point"]
                    for p in point:
                        if p['option']['value'] == v['value']:
                            p['num'] = p['num'] + 1
            if v.get("item_type") == "checkbox_option":
                # 处理多选
                if not item_map.get(v['item_name']):
                    point = {o['value']: {"option": o, "num": 0} for o in v.get("payload", {}).get("options", [])}
                    for value in v["value"]:
                        point[value]["num"] = point[value]["num"] + 1
                    item_map[v['item_name']] = {
                        "item_name": v['item_name'],
                        "point": list(point.values())
                    }
                else:
                    point = item_map[v['item_name']]["point"]
                    for p in point:
                        if p['option']['value'] in v['value']:
                            p['num'] = p['num'] + 1
            if v.get("item_type") == "raw_text":
                # 处理文本分词
                if not word_cloud.get(v['item_name']):
                    # 首次
                    value = v['value']
                    if value:
                        res = jieba.cut(value)
                        word_cloud[v['item_name']] = list(res)
                else:
                    value = v['value']
                    if value:
                        res = jieba.cut(value)
                        word_cloud[v['item_name']] = word_cloud[v['item_name']] + list(res)

    # word_cloud 转成数组新式
    word_cloud = [{"item_name": k,
                   "value":
                       [
                           {"word": i[0],
                            "num": i[1]}
                           for i in Counter(v).items()]} for k, v in
                  word_cloud.items()
                  ]

    redis_cli.set("form_service:{}:word_cloud".format(meta_name), json.dumps(word_cloud))
    redis_cli.set("form_service:{}:map".format(meta_name), json.dumps(list(item_map.values())))


def user_forms_num(username):
    from app.utils.mongodb import mongo
    try:
        total_datas = mongo.db.form.find(
            {'meta.guider': {'$in': [username]}, 'using': {'$in': [True]}})
    except Exception as e:
        return None, None, None, CustomError(500, 500, str(e))
    try:
        has_submitted_datas = mongo.db.form.find(
            {'meta.guider': {'$in': [username]}, 'using': {'$in': [True]}, 'status': {'$in': ['已完成']}})
    except Exception as e:
        return None, None, None, CustomError(500, 500, str(e))
    try:
        to_be_submitted_data = mongo.db.form.find(
            {'meta.guider': {'$in': [username]}, 'using': {'$in': [True]}, 'status': {'$in': ['待提交']}})
    except Exception as e:
        return None, None, None, CustomError(500, 500, str(e))
    return total_datas.count(), has_submitted_datas.count(), to_be_submitted_data.count(), None


@sub_kafka('form_service')
def form_service_receiver(message):
    method = message.get("method")
    if not method:
        return
    if method == 'add_form':
        calculate_map(message.get("args", {}).get("form", {}).get("bind_meta_name"))
        lesson_record_service.change_user_lesson_record_num(message.get("args", {}).get("username"))
    if method == 'repulse_form':
        lesson_record_service.change_user_lesson_record_num(message.get("args", {}).get("username"))
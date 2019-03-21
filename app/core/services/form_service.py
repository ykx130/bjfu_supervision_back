import json
import jieba
from collections import Counter
from flask_login import current_user
from datetime import datetime
from app.core.models.form import Form, Value
from app.core.models.lesson import Term
from app.core.services import lesson_record_service
from app.utils.url_condition.url_condition_mongodb import *
from app.utils.Error import CustomError
from app.streaming import sub_kafka, send_kafka_message
from app import redis_cli


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


def user_forms_num(username, term):
    from app.utils.mongodb import mongo
    if term is None:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    try:
        total_datas = mongo.db.form.find(
            {'meta.guider': {'$in': [username]}, 'using': {'$in': [True]}, 'meta.term': {'$in': [term]}})
    except Exception as e:
        return None, None, None, CustomError(500, 500, str(e))
    try:
        has_submitted_datas = mongo.db.form.find(
            {'meta.guider': {'$in': [username]}, 'using': {'$in': [True]}, 'status': {'$in': ['已完成']},
             'meta.term': {'$in': [term]}})
    except Exception as e:
        return None, None, None, CustomError(500, 500, str(e))
    try:
        to_be_submitted_data = mongo.db.form.find(
            {'meta.guider': {'$in': [username]}, 'using': {'$in': [True]}, 'status': {'$in': ['待提交']},
             'meta.term': {'$in': [term]}})
    except Exception as e:
        return None, None, None, CustomError(500, 500, str(e))
    return total_datas.count(), has_submitted_datas.count(), to_be_submitted_data.count(), None


def get_submitted_form_num(term=None):
    from app.utils.mongodb import mongo
    if term is None:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    try:
        submitted_forms = mongo.db.form.find(
            {'using': {'$in': [True]}, 'status': {'$in': ['已完成']}, 'meta.term': {'$in': [term]}})
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return submitted_forms.count(), None


def get_wait_submitted_form_num(term=None):
    from app.utils.mongodb import mongo
    if term is None:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    try:
        wait_submitted_forms = mongo.db.form.find(
            {'using': {'$in': [True]}, 'status': {'$in': ['待提交']}, 'meta.term': {'$in': [term]}})
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return wait_submitted_forms.count(), None


def find_form_unit_num(unit, term=None):
    from app.utils.mongodb import mongo
    if term is None:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    try:
        submitted_forms = mongo.db.form.find(
            {'using': {'$in': [True]}, 'status': {'$in': ['已完成']}, 'meta.term': {'$in': [term]},
             'meta.lesson.lesson_teacher_unit': {'$in': [unit]}})
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return submitted_forms.count(), None


def update_page_data():
    (submitted_form_num, err) = get_submitted_form_num()
    if err is not None:
        raise err
    (wait_submitted_form_num, err) = get_wait_submitted_form_num()
    if err is not None:
        raise err
    units = ['林学院', '水土保持学院', '生物科学与技术学院', '园林学院', '经济管理学院', '工学院',
             '理学院', '信息学院', '人文社会科学学院', '外语学院', '材料科学与技术学院',
             '自然保护区学院', '环境科学与工程学院', '艺术设计学院', '体育教学部', '马克思主义学院']
    for unit in units:
        (unit_num, err) = find_form_unit_num(unit)
        if err is not None:
            raise err
        redis_cli.set('sys:form_num:{unit}'.format(unit=unit), json.dumps(unit_num))
    redis_cli.set("sys:submitted_form", json.dumps(submitted_form_num))
    redis_cli.set("sys:wait_submitted_form", json.dumps(wait_submitted_form_num))


def lesson_forms_num(lesson_id):
    from app.utils.mongodb import mongo
    try:
        lesson_forms = mongo.db.form.find(
            {'meta.lesson.lesson_id': {'$in': [lesson_id]}, 'using': {'$in': [True]}, 'status': {'$in': ['已完成']}})
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return lesson_forms.count(), None


@sub_kafka('form_service')
def form_service_receiver(message):
    method = message.get("method")
    if not method:
        return
    if method == 'add_form' or method == 'repulse_form':
        calculate_map(message.get("args", {}).get("form", {}).get("bind_meta_name"))
        update_page_data()

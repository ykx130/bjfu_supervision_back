from app.core.services import form_service
from app.utils.url_condition.url_args_to_dict import args_to_dict
from app.core.services import form_meta_service
from app.streaming import send_kafka_message
from app import redis_cli
import json


def insert_form(request):
    form = form_service.request_to_class(request)
    (ifSuccess, err) = form_service.insert_form(form)
    if err is not None:
        return False, err
    form_model, err = form_service.to_json_dict(form.model)
    lesson_id = form.meta.get("lesson", {}).get("lesson_id", None)
    if err is not None:
        return False, err
    send_kafka_message(topic='form_service',
                       method='add_form',
                       term=form.meta.get('term', None),
                       username=form.meta.get('guider', None),
                       form=form_model,
                       lesson_id=lesson_id)

    form_service.push_new_form_message(form_model)
    return ifSuccess, None


def find_forms(condition=None):
    condition_fin = args_to_dict(condition)
    (forms, num, err) = form_service.find_forms(condition_fin)
    if err is not None:
        return None, None, err
    forms_model = list()
    for form in forms:
        (form_model, err) = form_service.to_json_dict(form)
        if err is not None:
            return None, None, err
        forms_model.append(form_model)
    return forms_model, num, None


def find_form(_id):
    (form, err) = form_service.find_form(_id)
    if err is not None:
        return None, err
    form_model = form_service.object_to_str(form)
    return form_model, None


def delete_form(condition=None):
    (ifSuccess, err) = form_service.delete_form(condition)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_form(condition=None, change_item=None):
    (ifSuccess, err) = form_service.update_form(condition, change_item)
    if err is not None:
        return False, err
    if 'status' in change_item:
        (form, err) = form_service.find_form(condition.get('_id'))
        if err is not None:
            return False, err
        (form_model, err) = form_service.to_json_dict(form)
        if err is not None:
            return False, err
        lesson_id = form.meta.get("lesson", {}).get("lesson_id", None)
        if change_item.get('status') == '待提交':
            send_kafka_message(topic='form_service',
                               method='repulse_form',
                               lesson_id=lesson_id)
            form_service.push_put_back_form_message(form_model)
        if change_item.get('status') == '已提交':
            send_kafka_message(topic='form_service',
                               method='add_form',
                               lesson_id=lesson_id)

    return ifSuccess, None


def get_form_map(meta_name):
    item_map = []
    word_cloud = []
    if redis_cli.exists("form_service:{}:map".format(meta_name)):
        item_map = json.loads(redis_cli.get("form_service:{}:map".format(meta_name)))
    if redis_cli.exists("form_service:{}:word_cloud".format(meta_name)):
        word_cloud = json.loads(redis_cli.get("form_service:{}:word_cloud".format(meta_name)))

    return {
        "item_map": item_map,
        "word_cloud": word_cloud
    }

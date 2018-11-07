from app.core.models.consult import Consult, ConsultType
from app.core.models.lesson import Term
from datetime import datetime
from flask_login import current_user
from app.utils.mysql import db
from app.utils.Error import CustomError
from app.streaming import sub_kafka, send_kafka_message


def find_consults(condition):
    try:
        consults = Consult.consults(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = consults.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def insert_consult(request_json):
    consult = Consult()
    consult.state = "待协调"
    consult.term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    consult.requester_username = current_user.username
    consult.submit_time = datetime.now()
    for key, value in request_json.items():
        if hasattr(consult, key):
            setattr(consult, key, value)
    db.session.add(consult)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_consult(id, request_json):
    try:
        consult = Consult.query.filter(Consult.id == int(id)).filter(Consult.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if consult is None:
        return False, CustomError(404, 404, 'consult not found')
    consult.state = "已协调"
    consult.responsor_username = current_user.username
    consult.answer_time = datetime.now()
    for key, value in request_json.items():
        if hasattr(consult, key):
            setattr(consult, key, value)
    db.session.add(consult)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def find_consult(id):
    try:
        consult = Consult.query.filter(Consult.id == int(id)).filter(Consult.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if consult is None:
        return None, CustomError(404, 404, 'consult not found')
    return consult, None


def delete_consult(id):
    try:
        consult = Consult.query.filter(Consult.id == int(id)).filter(Consult.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if consult is None:
        return False, CustomError(404, 404, 'consult not found')
    consult.using = False
    db.session.add(consult)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def consult_to_dict(consult):
    try:
        consult_dict = {
            'id': consult.id,
            'type': consult.type,
            'requester_username': consult.requester_username,
            'submit_time': str(consult.submit_time),
            'answer_time': str(consult.answer_time),
            'term': consult.term,
            'state': consult.state,
            'meta_description': consult.meta_description,
            'phone': consult.phone,
            'responsor_username': consult.responsor_username,
            'content': consult.content
        }
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    return consult_dict, None


def find_consult_types(condition):
    try:
        consult_types = ConsultType.consult_types(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = consult_types.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def insert_consult_type(request_json):
    consult_type = ConsultType()
    for key, value in request_json.items():
        if hasattr(consult_type, key):
            setattr(consult_type, key, value)
    db.session.add(consult_type)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_consult_type(id, request_json):
    try:
        consult_type = ConsultType.query.filter(ConsultType.id == int(id)).filter(ConsultType.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if consult_type is None:
        return False, CustomError(404, 404, 'consult not found')
    for key, value in request_json.items():
        if hasattr(consult_type, key):
            setattr(consult_type, key, value)
    db.session.add(consult_type)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def find_consult_type(id):
    try:
        consult_type = ConsultType.query.filter(ConsultType.id == int(id)).filter(ConsultType.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return consult_type, None


def delete_consult_type(id):
    try:
        consult_type = ConsultType.query.filter(ConsultType.id == int(id)).filter(ConsultType.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if consult_type is None:
        return False, CustomError(404, 404, 'consult not found')
    consult_type.using = False
    db.session.add(consult_type)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def consult_type_to_dict(consult_type):
    try:
        consult_type_dict = {
            'id': consult_type.id,
            'name': consult_type.name
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return consult_type_dict, None


def push_consult_reply_message(consult):
    """
    发送咨询回复的消息
    :param form_model:
    :return:
    """
    tmpl = "咨询 {meta_description} 被回复, 回复内容{content}"
    send_kafka_message(topic="notice_service", method="send_msg",
                       username=consult.get("requester_username"),
                       msg={
                           "title": "咨询协调",
                           "body": tmpl.format(
                               meta_description=consult.get("meta_description"),
                               content=consult.get("content")
                           )
                       }
                       )

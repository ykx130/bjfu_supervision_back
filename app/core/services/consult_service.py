from app.core.models.consult import Consult, ConsultType
from app.core.models.lesson import Term
from datetime import datetime
from flask_login import current_user
from app.utils.mysql import db

def find_consults(condition):
    try:
        consults = Consult.consults(condition)
    except Exception as e:
        return None, None, e
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
        return False, e
    return True, None


def update_consult(id, request_json):
    try:
        consult = Consult.query.filter(Consult.id == int(id)).filter(Consult.using == True).first()
    except Exception as e:
        return False, e
    if consult is None:
        return False, None
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
        return False, e
    return True, None


def find_consult(id):
    try:
        consult = Consult.query.filter(Consult.id == int(id)).filter(Consult.using == True).first()
    except Exception as e:
        return None, e
    return consult, None


def delete_consult(id):
    try:
        consult = Consult.query.filter(Consult.id == int(id)).filter(Consult.using == True).first()
    except Exception as e:
        return False, e
    if consult is None:
        return False, None
    consult.using = False
    db.session.add(consult)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def consult_to_dict(consult):
    return {
        'id': consult.id,
        'type': consult.type,
        'requester_username': consult.requester_username,
        'submit_time': consult.submit_time,
        'answer_time': consult.answer_time,
        'term': consult.term,
        'state': consult.state,
        'meta_description': consult.meta_description,
        'phone': consult.phone,
        'responsor_username': consult.responsor_username,
        'content': consult.content
    }


def find_consult_types(condition):
    try:
        consult_types = ConsultType.consult_types(condition)
    except Exception as e:
        return None, None, e
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
        return False, e
    return True, None


def update_consult_type(id, request_json):
    try:
        consult_type = ConsultType.query.filter(ConsultType.id == int(id)).filter(ConsultType.using == True).first()
    except Exception as e:
        return False, e
    if consult_type is None:
        return False, None
    for key, value in request_json.items():
        if hasattr(consult_type, key):
            setattr(consult_type, key, value)
    db.session.add(consult_type)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def find_consult_type(id):
    try:
        consult_type = ConsultType.query.filter(ConsultType.id == int(id)).filter(ConsultType.using == True).first()
    except Exception as e:
        return None, e
    return consult_type, None


def delete_consult_type(id):
    try:
        consult_type = ConsultType.query.filter(ConsultType.id == int(id)).filter(ConsultType.using == True).first()
    except Exception as e:
        return False, e
    if consult_type is None:
        return False, None
    consult_type.using = False
    db.session.add(consult_type)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def consult_type_to_dict(consult_type):
    return {
        'id': consult_type.id,
        'name': consult_type.name
    }

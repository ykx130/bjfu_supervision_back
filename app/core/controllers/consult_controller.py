from app.core.services import consult_service
from app.utils.url_condition.url_args_to_dict import args_to_dict


def find_consults(condition):
    condition_fin = args_to_dict(condition)
    (consults, num, err) = consult_service.find_consults(condition_fin)
    if err is not None:
        return None, None, err
    consults_model = list()
    for consult in consults:
        (consult_model, err) = consult_service.consult_to_dict(consult)
        if err is not None:
            return None, None, err
        consults_model.append(consult_model)
    return consults_model, num, None


def insert_consult(request_json):
    (ifSuccess, err) = consult_service.insert_consult(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_consult(id, request_json):
    (ifSuccess, err) = consult_service.update_consult(id, request_json)
    if err is not None:
        return False, err
    (consult, err) = consult_service.find_consult(id)

    (consult_model, err) = consult_service.consult_to_dict(consult)
    consult.push_consult_reply_message(consult_model)

    return ifSuccess, None


def find_consult(id):
    (consult, err) = consult_service.find_consult(id)
    if err is not None:
        return None, err
    (consult_model, err) = consult_service.consult_to_dict(consult)
    if err is not None:
        return None, err
    return consult_model, None


def delete_consult(id):
    (ifSuccess, err) = consult_service.delete_consult(id)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_consult_types(condition):
    condition_fin = args_to_dict(condition)
    (consult_types, num, err) = consult_service.find_consult_types(condition_fin)
    if err is not None:
        return None, None, err
    consult_types_model = list()
    for consult_type in consult_types:
        (consult_type_model, err) = consult_service.consult_type_to_dict(consult_type)
        if err is not None:
            return None, None, err
        consult_types_model.append(consult_type_model)
    return consult_types_model, num, None


def insert_consult_type(request_json):
    (ifSuccess, err) = consult_service.insert_consult_type(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_consult_type(id, request_json):
    (ifSuccess, err) = consult_service.update_consult_type(id, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_consult_type(id):
    (consult_type, err) = consult_service.find_consult_type(id)
    if err is not None:
        return None, err
    (consult_type_model, err) = consult_service.consult_type_to_dict(consult_type)
    if err is not None:
        return None, err
    return consult_type_model, None


def delete_consult_type(id):
    (ifSuccess, err) = consult_service.delete_consult_type(id)
    if err is not None:
        return False, err
    return ifSuccess, None


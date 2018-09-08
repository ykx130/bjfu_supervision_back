from app.core.services import consult_service


def find_consults(condition):
    (consults, num, err) = consult_service.find_consults(condition)
    return consults, num, err


def insert_consult(request_json):
    (ifSuccess, err) = consult_service.insert_consult(request_json)
    return ifSuccess, err


def update_consult(id, request_json):
    (ifSuccess, err) = consult_service.update_consult(id, request_json)
    return ifSuccess, err


def find_consult(id):
    (consult, err) = consult_service.find_consult(id)
    return consult, err


def delete_consult(id):
    (ifSuccess, err) = consult_service.delete_consult(id)
    return ifSuccess, err


def consult_to_dict(consult):
    return consult_service.consult_to_dict(consult)


def find_consult_types(condition):
    (consult_types, num, err) = consult_service.find_consult_types(condition)
    return consult_types, num, err


def insert_consult_type(request_json):
    (ifSuccess, err) = consult_service.insert_consult_type(request_json)
    return ifSuccess, err


def update_consult_type(id, request_json):
    (ifSuccess, err) = consult_service.update_consult_type(id, request_json)
    return ifSuccess, err


def find_consult_type(id):
    (consult_type, err) = consult_service.find_consult_type(id)
    return consult_type, err


def delete_consult_type(id):
    (ifSuccess, err) = consult_service.delete_consult_type(id)
    return ifSuccess, err


def consult_type_to_dict(consult_type):
    return consult_service.consult_type_to_dict(consult_type)

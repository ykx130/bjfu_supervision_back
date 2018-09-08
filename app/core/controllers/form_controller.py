from app.core.services import form_service


def insert_form(mongo, form):
    (ifSuccess, err) = form_service.insert_form(mongo, form)
    return ifSuccess, err


def find_forms(mongo, condition=None):
    (forms, err) = form_service.find_forms(mongo, condition)
    return forms, err


def find_form(mongo, _id):
    (form, err) = form_service.find_form(mongo, _id)
    return form, err


def delete_form(mongo, condition=None):
    (ifSuccess, err) = form_service.delete_form(mongo, condition)
    return ifSuccess, err


def update_form(mongo, condition=None, change_item=None):
    (ifSuccess, err) = form_service.update_form(mongo, condition, change_item)
    return ifSuccess, err


def to_json_list(form):
    return form_service.to_json_list(form)


def request_to_class(json_request):
    return form_service.request_to_class(json_request)

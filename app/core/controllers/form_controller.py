from app.core.services import form_service
from app.core.services import form_meta_service


def insert_form(request):
    form = form_service.request_to_class(request)
    (ifSuccess, err) = form_service.insert_form(form)
    return ifSuccess, err


def find_forms(condition=None):
    (forms, num, err) = form_service.find_forms(condition)
    if err is not None:
        return [], 0, err
    forms_model = [form_service.to_json_list(form) for form in forms]
    return forms_model, num, err


def find_form(_id):
    (form, err) = form_service.find_form(_id)
    if err is not None:
        return None, err
    if form is None:
        return None, err
    form_model = form_service.to_json_list(form)
    return form_model, err


def delete_form(condition=None):
    (ifSuccess, err) = form_service.delete_form(condition)
    return ifSuccess, err


def update_form(condition=None, change_item=None):
    (ifSuccess, err) = form_service.update_form(condition, change_item)
    return ifSuccess, err

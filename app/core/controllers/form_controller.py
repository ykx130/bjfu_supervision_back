from app.core.services import form_service
from app.core.services import form_meta_service
from app.streaming import send_kafka_message


def insert_form(request):
    form = form_service.request_to_class(request)
    (ifSuccess, err) = form_service.insert_form(form)
    if err is not None:
        return False, err
    form_model, err = form_service.to_json_dict(form.model)
    if err is not None:
        return False, err
    send_kafka_message(topic='form_service',
                       method='add_form',
                       form=form_model)
    return ifSuccess, None


def find_forms(condition=None):
    (forms, num, err) = form_service.find_forms(condition)
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
    return ifSuccess, None

from app.core.services import model_lesson_service
from app.core.services import lesson_service


def find_model_lesson(id):
    (model_lesson, err) = model_lesson_service.find_model_lesson(id)
    if err is not None:
        return None, err
    (lesson, err) = lesson_service.find_lesson(model_lesson.lesson_id)
    if err is not None:
        return None, err
    (model, err) = model_lesson_service.model_lesson_dict(lesson, model_lesson)
    if err is not None:
        return None, err
    return model, None


def find_model_lessons(condition):
    (model_lessons, num, err) = model_lesson_service.find_model_lessons(condition)
    if err is not None:
        return None, None, err
    models = list()
    for model_lesson in model_lessons:
        (lesson, err) = lesson_service.find_lesson(model_lesson.lesson_id)
        if err is not None:
            return None, None, err
        (model, err) = model_lesson_service.model_lesson_dict(lesson, model_lesson)
        if err is not None:
            return None, None, err
        models.append(model)
    return models, num, None


def insert_model_lesson(request_json):
    (ifSuccess, err) = model_lesson_service.insert_model_lesson(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def insert_model_lessons(request_json):
    (ifSuccess, err) = model_lesson_service.insert_model_lessons(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def delete_model_lesson(id):
    (ifSuccess, err) = model_lesson_service.delete_model_lesson(id)
    if err is not None:
        return False, err
    return ifSuccess, None


def delete_model_lessons(request_json):
    (ifSuccess, err) = model_lesson_service.delete_model_lessons(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_model_lesson(id, request_json):
    (ifSuccess, err) = model_lesson_service.update_model_lesson(id, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def model_lesson_vote(id, vote=True):
    (ifSuccess, err) = model_lesson_service.model_lesson_vote(id, vote)
    if err is not None:
        return False, err
    return ifSuccess, None


def export_lesson_excel(request_json):
    (filename, err) = model_lesson_service.export_lesson_excel(request_json)
    if err is not None:
        return None, err
    return filename, None


def import_lesson_excel(request_json):
    (ifSuccess, err) = model_lesson_service.import_lesson_excel(request_json)
    if err is not None:
        return False, err
    return True, None

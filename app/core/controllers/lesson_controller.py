from app.core.services import lesson_service
from app.utils.url_condition.url_args_to_dict import args_to_dict


def update_database():
    lesson_service.update_database()


def find_lesson(id):
    (lesson, err) = lesson_service.find_lesson(id)
    if err is not None:
        return None, err
    (lesson_model, err) = lesson_service.lesson_to_model(lesson)
    if err is not None:
        return None, err
    return lesson_model, err


def has_lesson(id):
    (ifSuccess, err) = lesson_service.has_lesson(id)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_lessons(condition):
    condition_fin = args_to_dict(condition)
    (lessons, num, err) = lesson_service.find_lessons(condition_fin)
    if err is not None:
        return None, None, err
    lessons_model = list()
    for lesson in lessons:
        (lesson_model, err) = lesson_service.lesson_to_model(lesson)
        if err is not None:
            return None, None, err
        lessons_model.append(lesson_model)
    return lessons_model, num, None


def change_lesson(id, request_json):
    (ifSuccess, err) = lesson_service.change_lesson(id, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_terms(condition):
    condition_fin = args_to_dict(condition)
    (terms, num, err) = lesson_service.find_terms(condition_fin)
    if err is not None:
        return None, None, err
    terms_model = list()
    for term in terms:
        (term_model, err) = lesson_service.term_to_dict(term)
        if err is not None:
            return None, None, err
        terms_model.append(term_model)
    return terms_model, num, None


def find_term(term_name):
    (term, err) = lesson_service.find_term(term_name)
    if err is not None:
        return None, err
    (term_model, err) = lesson_service.term_to_dict(term)
    if err is not None:
        return None, err
    return term_model, None


def find_now_term():
    (term, err) = lesson_service.find_now_term()
    if err is not None:
        return None, err
    (term_model, err) = lesson_service.term_to_dict(term)
    if err is not None:
        return None, err
    return term_model, err

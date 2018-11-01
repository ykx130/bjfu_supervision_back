from app.core.services import lesson_record_service, lesson_service


def find_lesson_records_history(condition):
    (lesson_records, num, err) = lesson_record_service.find_lesson_records_history(condition)
    if err is not None:
        return None, None, err
    lesson_records_model = list()
    for lesson_record in lesson_records:
        (lesson_record_model, err) = lesson_record_service.lesson_record_to_dict(lesson_record)
        if err is not None:
            return None, None, err
        lesson_records_model.append(lesson_record_model)
    return lesson_records_model, num, None


def find_term_lesson_records(condition):
    if 'term' in condition:
        term = condition.get('term')
    else:
        (term, err) = lesson_service.find_now_term()
        if err is not None:
            return None, err
        term = term.name
    (lesson_records, num, err) = lesson_record_service.find_term_lesson_records(term, condition)
    if err is not None:
        return None, None, err
    lesson_records_model = list()
    for lesson_record in lesson_records:
        (lesson_record_model, err) = lesson_record_service.lesson_record_to_dict(lesson_record)
        if err is not None:
            return None, None, err
        lesson_records_model.append(lesson_record_model)
    return lesson_records_model, num, None


def find_lesson_record(username, term=None):
    if term is None:
        (term, err) = lesson_service.find_now_term()
        if err is not None:
            return None, err
        term = term.name
    (lesson_record, err) = lesson_record_service.find_lesson_record(username, term)
    if err is not None:
        return None, err
    (lesson_record_model, err) = lesson_record_service.lesson_record_to_dict(lesson_record)
    if err is not None:
        return None, err


def find_lesson_record_history(username, condition):
    (lesson_records, num, err) = lesson_record_service.find_lesson_record_history(username, condition)
    if err is not None:
        return None, None, err
    lesson_records_model = list()
    for lesson_record in lesson_records:
        (lesson_record_model, err) = lesson_record_service.lesson_record_to_dict(lesson_record)
        if err is not None:
            return None, None, err
        lesson_records_model.append(lesson_record_model)
    return lesson_records_model, num, None


def insert_lesson_record(request_json):
    (ifSuccess, err) = lesson_record_service.insert_lesson_record(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def delete_lesson_record(username, term):
    (ifSuccess, err) = lesson_record_service.delete_lesson_record(username, term)
    if err is not None:
        return False, err
    return True, None


def update_lesson_record(username, term, request_json):
    (ifSuccess, err) = lesson_record_service.update_lesson_record(username, term, request_json)
    if err is not None:
        return False, err
    return True, None

from app.core.services import lesson_service


def update_database():
    lesson_service.update_database()


def lesson_to_model(lesson):
    return lesson_service.lesson_to_model(lesson)


def find_lesson(id):
    (lesson, err) = lesson_service.find_lesson(id)
    lesson_model = lesson_service.lesson_to_model(lesson)
    return lesson_model, err


def has_lesson(id):
    (ifSuccess, err) = lesson_service.has_lesson(id)
    return ifSuccess, err


def find_lessons(condition):
    (lessons, num, err) = lesson_service.find_lessons(condition)
    if err is not None:
        return None, None, err
    lessons_model = [lesson_service.lesson_to_model(lesson) for lesson in lessons]
    return lessons_model, num, err


def change_lesson(id, request_json):
    (ifSuccess, err) = lesson_service.change_lesson(id, request_json)
    return ifSuccess, err


def find_terms(condition):
    (terms, num, err) = lesson_service.find_terms(condition)
    return terms, num, err


def find_term(term_name):
    (term, err) = lesson_service.find_term(term_name)
    return term, err


def find_now_term():
    (term, err) = lesson_service.find_now_term()
    return term, err

from app.core.services import notice_lesson_service
from app.core.services import lesson_service


def find_notice_lesson(id):
    notice_lesson, err = notice_lesson_service.find_notice_lesson(id)
    if err is not None:
        return None, err
    notice_lesson_model = notice_lesson_service.notice_lesson_to_dict(notice_lesson)
    return notice_lesson_model, err


def find_notice_lessons(condition):
    (notice_lessons, num, err) = notice_lesson_service.find_notice_lessons(condition)
    if err is not None:
        return None, None, err
    notice_lessons_model = list()
    for notice_lesson in notice_lessons:
        lesson, err = lesson_service.find_lesson(notice_lesson.lesson_id)
        if err is not None:
            return None, None, err
        notice_lesson_model = notice_lesson_service.notice_lesson_to_dict(lesson, notice_lesson)
        notice_lessons_model.append(notice_lesson_model)
    return notice_lessons_model, num, err


def insert_notice_lesson(request_json):
    (ifSuccess, err) = notice_lesson_service.insert_notice_lesson(request_json)
    return ifSuccess, err


def insert_notice_lessons(request_json):
    (ifSuccess, err) = notice_lesson_service.insert_notice_lessons(request_json)
    return ifSuccess, err


def delete_notice_lesson(id):
    (ifSuccess, err) = notice_lesson_service.delete_notice_lesson(id)
    return ifSuccess, err


def delete_notice_lessons(request_json):
    (ifSuccess, err) = notice_lesson_service.delete_notice_lessons(request_json)
    return ifSuccess, err


def update_notice_lesson(id, request_json):
    (ifSuccess, err) = notice_lesson_service.update_notice_lesson(id, request_json)
    return ifSuccess, err

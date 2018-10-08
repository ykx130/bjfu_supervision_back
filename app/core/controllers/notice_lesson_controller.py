from app.core.services import notice_lesson_service


def find_notice_lesson(id):
    notice_lesson, err = notice_lesson_service.find_notice_lesson(id)
    if err is not None:
        return None, err
    notice_lesson_model = notice_lesson_service.notice_lesson_to_dict(notice_lesson)
    return notice_lesson


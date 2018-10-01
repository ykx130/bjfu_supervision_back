from app.core.services import lesson_record_service


def find_lesson_records(condition):
    (lesson_records, total, err) = lesson_record_service.find_lesson_records(condition)
    if err is not None:
        return [], 0, err
    lesson_record_model = [lesson_record_service.lesson_record_to_dict(lesson_record) for lesson_record in
                           lesson_records]
    return lesson_record_model, total, err


def find_lesson_record(id):
    (lesson_record, err) = lesson_record_service.find_lesson_record(id)
    if err is not None:
        return None, err
    lesson_record_model = lesson_record_service.lesson_record_to_dict(lesson_record)
    return lesson_record_model, err

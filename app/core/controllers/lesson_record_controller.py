from app.core.services import lesson_record_service


def find_lesson_records(condition):
    (lesson_records, total, err) = lesson_record_service.find_lesson_records(condition)
    if err is not None:
        return None, None, err
    lesson_records_model = list()
    for lesson_record in lesson_records:
        (lesson_record_model, err) = lesson_record_service.lesson_record_to_dict(lesson_record)
        if err is not None:
            return None, None, err
        lesson_records_model.append(lesson_record_model)
    return lesson_records_model, total, None


def find_lesson_record(id):
    (lesson_record, err) = lesson_record_service.find_lesson_record(id)
    if err is not None:
        return None, err
    (lesson_record_model, err) = lesson_record_service.lesson_record_to_dict(lesson_record)
    if err is not None:
        return None, err
    return lesson_record_model, None

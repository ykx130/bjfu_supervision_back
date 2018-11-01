from app.core.models.lesson import LessonRecord
from app.utils.mysql import db
from app.utils.Error import CustomError
from app.core.services import form_service, user_service, lesson_service


def find_lesson_records_history(condition):
    try:
        lesson_records = LessonRecord.lesson_records(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = lesson_records.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_term_lesson_records(term, condition):
    try:
        lesson_records = LessonRecord.lesson_records(condition).filter(LessonRecord.term == term)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = lesson_records.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_lesson_record_history(username, condition):
    try:
        lesson_records = LessonRecord.lesson_records(condition).filter(LessonRecord.username == username)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = lesson_records.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_lesson_record(username, term):
    try:
        lesson_record = LessonRecord.query.filter(LessonRecord.username == username).filter(
            LessonRecord.term == term).filter(LessonRecord.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if lesson_record is None:
        return None, CustomError(404, 404, 'lesson record not found')
    return lesson_record, None


def insert_lesson_record(request_json):
    lesson_record = LessonRecord()
    for key, value in request_json.items():
        if hasattr(lesson_record, key):
            setattr(lesson_record, key, value)
    try:
        db.session.add(lesson_record)
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_lesson_record(username, term):
    try:
        lesson_record = LessonRecord.query.filter(LessonRecord.username == username).filter(
            LessonRecord.using == True).filter(LessonRecord.term == term).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if lesson_record is None:
        return False, CustomError(404, 404, 'lesson record not found')
    lesson_record.using = False
    db.session.add(lesson_record)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_lesson_record(username, term, request_json):
    try:
        lesson_record = LessonRecord.query.filter(LessonRecord.username == username).filter(
            LessonRecord.using == True).filter(LessonRecord.term == term).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if lesson_record is None:
        return False, CustomError(404, 404, 'lesson record not found')
    for key, value in request_json:
        if hasattr(lesson_record, key):
            setattr(lesson_record, key, value)
    db.session.add(lesson_record)
    try:
        db.session.commit()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    return True, None


def change_user_lesson_record_num(username, term):
    (total_times, has_submitted_times, to_be_submitted_times, err) = form_service.user_forms_num(username)
    if err is not None:
        raise err
    (ifSuccess, err) = update_lesson_record(username, term,
                                            {'total_times': total_times, 'has_submitted': has_submitted_times,
                                             'to_be_submitted': to_be_submitted_times})
    if err is not None:
        raise err


def lesson_record_to_dict(lesson_record):
    try:
        lesson_record_dict = {
            'id': lesson_record.id,
            'username': lesson_record.username,
            'name': lesson_record.name,
            'term': lesson_record.term,
            'group_name': lesson_record.group_name,
            'to_be_submitted': lesson_record.to_be_submitted,
            'has_submitted': lesson_record.has_submitted,
            'total_times': lesson_record.total_times
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return lesson_record_dict, None

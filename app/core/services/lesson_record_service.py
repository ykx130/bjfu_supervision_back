from app.core.models.lesson import LessonRecord
from app.utils.mysql import db
from app.utils.Error import CustomError


def find_lesson_records(condition):
    try:
        lesson_records = LessonRecord.lesson_records(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = lesson_records.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_lesson_record(username):
    try:
        lesson_record = LessonRecord.query.filter(LessonRecord.username == username).filter(
            LessonRecord.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
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


def lesson_record_to_dict(lesson_record):
    try:
        lesson_record_dict = {
            'id': lesson_record.id,
            'username': lesson_record.username,
            'name': lesson_record.name,
            'group_name': lesson_record.group_name,
            'to_be_submitted': lesson_record.to_be_submitted,
            'has_submitted': lesson_record.has_submitted,
            'total_times': lesson_record.total_times
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return lesson_record_dict, None

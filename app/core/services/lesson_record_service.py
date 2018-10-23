from app.core.models.lesson import LessonRecord


def find_lesson_records(condition):
    try:
        lesson_records = LessonRecord.lesson_records(condition)
    except Exception as e:
        return None, None, e
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = lesson_records.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_lesson_record(id):
    try:
        lesson_record = LessonRecord.query.filter(LessonRecord.id == int(id)).filter(LessonRecord.using == True).first()
    except Exception as e:
        return None, e
    return lesson_record, None


def lesson_record_to_dict(lesson_record):
    return {
        'id': lesson_record.id,
        'username': lesson_record.username,
        'name': lesson_record.name,
        'group_name': lesson_record.group_name,
        'to_be_submitted': lesson_record.to_be_submitted,
        'has_submitted': lesson_record.has_submitted,
        'total_times': lesson_record.total_times
    }

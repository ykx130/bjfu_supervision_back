from app.core.models.lesson import ModelLesson
from app.utils.mysql import db


def find_model_lesson(id):
    model_lesson = ModelLesson.query.filter(id).first()
    if model_lesson is None:
        return None, 'not found'
    return model_lesson, None


def find_model_lessons(condition):
    model_lessons = ModelLesson.model_lessons(condition)
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = model_lessons.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def insert_model_lesson(request_json):
    model_lesson = ModelLesson()
    for key, value in request_json.items():
        if hasattr(model_lesson, key):
            setattr(model_lesson, key, value)
    db.session.add(model_lesson)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def update_model_lesson(id, request_json):
    model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
    if model_lesson is None:
        return False, 'not found'
    for key, value in request_json:
        if hasattr(model_lesson, key):
            setattr(model_lesson, key, value)
    db.session.add(model_lesson)
    try:
        db.session.commit(model_lesson)
    except Exception as e:
        return False, e
    return True, None


def delete_model_lesson(id):
    model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
    if model_lesson is None:
        return False, 'not found'
    model_lesson.using = True
    db.session.add(model_lesson)
    try:
        db.session.commit(model_lesson)
    except Exception as e:
        return False, e
    return True, None


def model_lesson_dict(lesson, model_lesson):
    try:
        model_dict = {
            'id': model_lesson.id if model_lesson is not None else None,
            'lesson_id': model_lesson.lesson_id if lesson is not None else None,
            'lesson_attribute': lesson.lesson_attribute if lesson is not None else None,
            'lesson_state': lesson.lesson_state if lesson is not None else None,
            'lesson_level': lesson.lesson_level if lesson is not None else None,
            'lesson_name': lesson.lesson_name,
            'lesson_teacher_id': lesson.lesson_teacher_id,
            'status': model_lesson.status,
            'votes': model_lesson.votes
        }
    except Exception as e:
        return None, e
    return model_lesson, None

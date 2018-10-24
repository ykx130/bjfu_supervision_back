from app.core.models.lesson import ModelLesson, Lesson
from app.utils.mysql import db


def find_model_lesson(id):
    model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
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
    lesson_id = request_json.get('lesson_id', None)
    if lesson_id is None:
        return False, 'lesson_id should be give'
    lesson = Lesson.query.filter(Lesson.lesson_id == lesson_id).filter(Lesson.using == True).first()
    if lesson is None:
        return False, 'not found'
    for key, value in request_json.items():
        if hasattr(model_lesson, key):
            setattr(model_lesson, key, value)
    status = request_json['status'] if 'status' in request_json else '推荐课'
    lesson.lesson_model = status
    db.session.add(model_lesson)
    db.session.add(lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.roll_back()
        return False, e
    return True, None


def update_model_lesson(id, request_json):
    model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
    lesson = Lesson.query.filter(Lesson.lesson_id == model_lesson.lesson_id).filter(Lesson.using == True).first()
    if lesson is None:
        return False, 'lesson not found'
    if model_lesson is None:
        return False, 'not found'
    for key, value in request_json:
        if hasattr(model_lesson, key):
            setattr(model_lesson, key, value)
    status = lesson.lesson_model if 'status' not in request_json else request_json['status']
    lesson.lesson_model = status
    db.session.add(model_lesson)
    db.session.add(lesson)
    try:
        db.session.commit(model_lesson)
    except Exception as e:
        db.session.roll_back()
        return False, e
    return True, None


def delete_model_lesson(id):
    model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
    lesson = Lesson.query.filter(Lesson.lesson_id == model_lesson.lesson_id).filter(Lesson.using == True).first()
    if lesson is None:
        return False, 'lesson not found'
    if model_lesson is None:
        return False, 'not found'
    model_lesson.using = True
    lesson.lesson_model = ''
    db.session.add(model_lesson)
    try:
        db.session.commit(model_lesson)
    except Exception as e:
        db.session.roll_back()
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
            'lesson_model': lesson.lesson_model if lesson is not None else None,
            'lesson_name': lesson.lesson_name,
            'lesson_teacher_id': lesson.lesson_teacher_id,
            'assign_group': model_lesson.assign_group,
            'status': model_lesson.status,
            'votes': model_lesson.votes,
            'notices': model_lesson.notices,
            'term': lesson.term if lesson is not None else None
        }
    except Exception as e:
        return None, e
    return model_dict, None


def change_model_lesson_notice(id, vote=True):
    model_lesson = ModelLesson.query.filter(ModelLesson.id == id).filter(ModelLesson.using == True)
    if model_lesson is None:
        return False, 'not found'
    if vote:
        model_lesson.votes = model_lesson.votes + 1
    model_lesson.notices = model_lesson.notices + 1
    db.session.add(model_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.roll_back()
        return False, e
    return True, None

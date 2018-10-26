from app.core.models.lesson import ModelLesson, Lesson
from app.utils.mysql import db
from app.utils.Error import CustomError


def find_model_lesson(id):
    try:
        model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if model_lesson is None:
        return None, CustomError(404, 404, 'model lesson not found')
    return model_lesson, None


def find_model_lessons(condition):
    try:
        model_lessons = ModelLesson.model_lessons(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = model_lessons.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def insert_model_lesson(request_json):
    model_lesson = ModelLesson()
    lesson_id = request_json.get('lesson_id', None)
    if lesson_id is None:
        return False, CustomError(500, 200, 'lesson_id should be given')
    try:
        lesson = Lesson.query.filter(Lesson.lesson_id == lesson_id).filter(Lesson.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if lesson is None:
        return False, CustomError(404, 404, 'lesson not found')
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
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def insert_model_lessons(request_json):
    lesson_ids = request_json.get('lesson_ids', None)
    if lesson_ids is None:
        return False, CustomError(500, 200, 'lesson_ids should be given')
    for lesson_id in lesson_ids:
        model_lesson = ModelLesson()
        try:
            lesson = Lesson.query.filter(Lesson.lesson_id == lesson_id).filter(Lesson.using == True).first()
        except Exception as e:
            db.session.rollback()
            return False, CustomError(500, 500, str(e))
        if lesson is None:
            db.session.rollback()
            return False, CustomError(404, 404, 'lesson not found')
        for key, value in request_json.items():
            if hasattr(model_lesson, key):
                setattr(model_lesson, key, value)
        model_lesson.lesson_id = lesson_id
        status = request_json['status'] if 'status' in request_json else '推荐课'
        lesson.lesson_model = status
        db.session.add(model_lesson)
        db.session.add(lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_model_lesson(id, request_json):
    try:
        model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
        lesson = Lesson.query.filter(Lesson.lesson_id == model_lesson.lesson_id).filter(Lesson.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if lesson is None:
        return False, CustomError(404, 404, 'lesson not found')
    if model_lesson is None:
        return False, CustomError(404, 404, 'model lesson not found')
    for key, value in request_json:
        if hasattr(model_lesson, key):
            setattr(model_lesson, key, value)
    status = lesson.lesson_model if 'status' not in request_json else request_json['status']
    lesson.lesson_model = status
    db.session.add(model_lesson)
    db.session.add(lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_model_lesson(id):
    try:
        model_lesson = ModelLesson.query.filter(ModelLesson.id == id).first()
        lesson = Lesson.query.filter(Lesson.lesson_id == model_lesson.lesson_id).filter(Lesson.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if lesson is None:
        return False, CustomError(404, 404, 'lesson not found')
    if model_lesson is None:
        return False, CustomError(404, 404, 'model lesson not found')
    model_lesson.using = True
    lesson.lesson_model = ''
    db.session.add(model_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_model_lessons(request_json):
    model_lesson_ids = request_json.get('model_lesson_ids', None)
    if model_lesson_ids is None:
        return False, CustomError(500, 200, 'model lesson ids should be given')
    for model_lesson_id in model_lesson_ids:
        try:
            model_lesson = ModelLesson.query.filter(ModelLesson.id == model_lesson_id).first()
            lesson = Lesson.query.filter(Lesson.lesson_id == model_lesson.lesson_id).filter(
                Lesson.using == True).first()
        except Exception as e:
            db.session.rollback()
            return False, CustomError(500, 500, str(e))
        if lesson is None:
            db.session.rollback()
            return False, CustomError(404, 404, 'lesson not found')
        if model_lesson is None:
            db.session.rollback()
            return False, CustomError(404, 404, 'model lesson not found')
        model_lesson.using = True
        lesson.lesson_model = ''
        db.session.add(model_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
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
        return None, CustomError(500, 500, str(e))
    return model_dict, None


def change_model_lesson_notice(id, vote=True):
    try:
        model_lesson = ModelLesson.query.filter(ModelLesson.id == id).filter(ModelLesson.using == True)
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if model_lesson is None:
        return False, CustomError(404, 404, 'model lesson not found')
    if vote:
        model_lesson.votes = model_lesson.votes + 1
    model_lesson.notices = model_lesson.notices + 1
    db.session.add(model_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None

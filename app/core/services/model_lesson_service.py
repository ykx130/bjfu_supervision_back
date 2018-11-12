from app.core.models.lesson import ModelLesson, Lesson, Term
from app.utils.mysql import db
from app.utils.Error import CustomError
import datetime
import pandas


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
    term = request_json.get('term', None)
    if not term:
        term = Term.query.order_by(
            Term.name.desc()).filter(Term.using == True).first().name
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
        status = request_json.get('status', '推荐课')
        lesson.lesson_model = status
        model_lesson.term = term
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
            'notices': lesson.notices,
            'term': lesson.term if lesson is not None else None
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return model_dict, None


def model_lesson_vote(id, vote=True):
    try:
        model_lesson = ModelLesson.query.filter(ModelLesson.id == id).filter(ModelLesson.using == True)
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if model_lesson is None:
        return False, CustomError(404, 404, 'model lesson not found')
    lesson = Lesson.query.filter(Lesson.lesson_id == model_lesson.lesson_id).filter(Lesson.using == True).first()
    if model_lesson is None:
        return False, CustomError(404, 404, 'lesson not found')
    if vote:
        model_lesson.votes = model_lesson.votes + 1
    lesson.notices = lesson.notices + 1
    db.session.add(model_lesson)
    db.session.add(lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True,


def import_lesson_excel(request_json):
    if 'filename' in request_json.files:
        from app import basedir
        filename = basedir + '/static/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
        file = request_json.files['filename']
        file.save(filename)
        df = pandas.read_excel(filename)
    else:
        return False, CustomError(500, 200, 'file must be given')
    column_dict = {'课程名称': 'lesson_name', '课程性质': 'lesson_attribute', '学分': 'lesson_grade', '开课学年': 'lesson_year',
                   '开课学期': 'lesson_semester', '任课教师名称': 'lesson_teacher_name', '任课教师所在学院': 'lesson_teacher_unit',
                   '指定小组': 'assign_group', '投票次数': 'votes', '提交次数': 'notices'}
    filter_list = ['lesson_name', 'lesson_teacher_name', 'lesson_semester', 'lesson_year', 'lesson_attribute',
                   'lesson_grade']
    row_num = df.shape[0]
    for i in range(0, row_num):
        lessons = Lesson.query
        for col_name_c, col_name_e in column_dict.items():
            if col_name_e in filter_list and hasattr(Lesson, col_name_e):
                lessons = lessons.filter(getattr(Lesson, col_name_e) == str(df.iloc[i][col_name_c]))
        lesson = lessons.first()
        if lesson is None:
            return False, CustomError(404, 404, 'lesson not found')
        model_lesson = ModelLesson()
        for col_name_c, col_name_e in column_dict.items():
            if hasattr(model_lesson, col_name_e):
                setattr(model_lesson, col_name_e, str(df.iloc[i][col_name_c]))
        model_lesson.lesson_id = lesson.lesson_id
        model_lesson.term = '_'.join([str(df.iloc[i]['开课学年']), str(df.iloc[i]['开课学期'])])
        db.session.add(model_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def export_lesson_excel(request_json):
    if 'model_lesson_ids' not in request_json:
        model_lessons = ModelLesson.query.filter(ModelLesson.using == True)
    else:
        model_lesson_ids = request_json['model_lesson_ids']
        model_lessons = ModelLesson.query.filter(ModelLesson.lesson_id.in_(model_lesson_ids)).filter(
            ModelLesson.using == True)
    column_dict = {'课程名称': 'lesson_name', '课程性质': 'lesson_attribute', '学分': 'lesson_grade', '开课学年': 'lesson_year',
                   '开课学期': 'lesson_semester', '任课教师名称': 'lesson_teacher_name', '任课教师所在学院': 'lesson_teacher_unit',
                   '指定小组': 'assign_group', '投票次数': 'votes', '提交次数': 'notices'}
    frame_dict = dict()
    for model_lesson in model_lessons:
        lesson = Lesson.query.filter(Lesson.lesson_id == model_lesson.lesson_id).first()
        if lesson is None:
            return None, CustomError(404, 404, 'lesson not found')
        for key, value in column_dict.items():
            excel_value = getattr(lesson, value) if hasattr(lesson, value) else getattr(model_lesson, value)
            if key not in frame_dict:
                frame_dict[key] = [excel_value]
            else:
                frame_dict[key].append(excel_value)
    try:
        frame = pandas.DataFrame(frame_dict)
        from app import basedir
        filename = basedir + '/static/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
        frame.to_excel(filename, sheet_name="123", index=False, header=True)
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return filename, None

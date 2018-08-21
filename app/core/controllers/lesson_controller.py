import pymysql
from app import db
import json
from app.core.models.lesson import Lesson, LessonCase, Term


def update_database():
    lesson_db = pymysql.connect(host="localhost", user="root", passwd="wshwoaini", db="lessons", charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor = lesson_db.cursor()

    cursor.execute("select distinct lesson_id,lesson_attribute, lesson_state, lesson_teacher_id, lesson_name, lesson_teacher_name, \
                   lesson_semester, lesson_level, lesson_teacher_unit, lesson_unit, lesson_year, lesson_type, lesson_class, lesson_attention_reason,\
                   lesson_model, lesson_grade, assign_group from lessons")
    datas = cursor.fetchall()
    for data in datas:
        teacher_name = data['lesson_teacher_name']
        teachers = data['lesson_teacher_name'].replace(' ', '').split(',')
        data['lesson_teacher_name'] = teachers
        teacher_ids = data['lesson_teacher_id'].replace(' ', '').split(',')
        data['lesson_teacher_id'] = teacher_ids
        teacher_units = data['lesson_teacher_unit'].replace(' ', '').split(',')
        data['lesson_teacher_unit'] = teacher_units
        for index in range(len(teachers)):
            lesson = Lesson()
            for k, v in data.items():
                try:
                    v = json.loads(v)
                except:
                    v = v
                if v is None or v is '':
                    continue
                if hasattr(lesson, k):
                    if type(v) is list:
                        setattr(lesson, k, v[index])
                    else:
                        setattr(lesson, k, v)
            db.session.add(lesson)
            db.session.commit()
            cursor.execute("select lesson_week, lesson_time, lesson_weekday, lesson_room from lessons where lesson_id \
                            ='{}' and lesson_teacher_name='{}'".format(data['lesson_id'], teacher_name))
            lesson_case_datas = cursor.fetchall()
            for lesson_case_data in lesson_case_datas:
                lesson_case = LessonCase()
                for k, v in lesson_case_data.items():
                    try:
                        v = json.loads(v)
                    except:
                        v = v
                    if v is None or v is '':
                        continue
                    if hasattr(lesson_case, k):
                        setattr(lesson_case, k, v)
                lesson_case.lesson_id = lesson.id
                db.session.add(lesson_case)
                db.session.commit()


def lesson_to_model(lesson):
    lesson_cases = [{"lesson_week": lesson_case.lesson_week, "lesson_time": lesson_case.lesson_time,
                     "lesson_weekday": lesson_case.lesson_weekday, "lesson_room": lesson_case.lesson_weekday} for
                    lesson_case in lesson.lesson_cases]
    lesson_model = {"lesson_id": lesson.lesson_id, "lesson_attribute": lesson.lesson_attribute,
                    "lesson_state": lesson.lesson_state, "lesson_teacher_id": lesson.lesson_teacher_id,
                    "lesson_name": lesson.lesson_name, "lesson_teacher_name": lesson.lesson_teacher_name,
                    "lesson_semester": lesson.lesson_semester, "lesson_level": lesson.lesson_level,
                    "lesson_teacher_unit": lesson.lesson_teacher_unit, "lesson_unit": lesson.lesson_unit,
                    "lesson_year": lesson.lesson_year, "lesson_type": lesson.lesson_type,
                    "lesson_class": lesson.lesson_class, "lesson_attention_reason": lesson.lesson_attention_reason,
                    "lesson_model": lesson.lesson_model, "lesson_grade": lesson.lesson_grade,
                    "assign_group": lesson.assgin_group, "lesson_cases": lesson_cases}
    return lesson_model


def find_lesson(id):
    try:
        lesson = Lesson.query.filter(Lesson.id == int(id)).first()
    except Exception as e:
        return None, e
    lesson_model = lesson_to_model(lesson)
    return lesson_model, None


def has_lesson(id):
    try:
        lesson = Lesson.query.filter(Lesson.id == id).first()
    except Exception as e:
        return None, e
    return False, None if lesson is None else True, None


def find_lessons(condition):
    try:
        lessons = Lesson.lessons(condition)
    except Exception as e:
        return None, None, e
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = lessons.paginate(page=int(page), per_page=int(per_page), error_out=False)
    lesson_page = pagination.items
    lesson_models = []
    for lesson in lesson_page:
        lesson_model = lesson_to_model(lesson)
        lesson_models.append(lesson_model)
    return lesson_models, pagination.total, None


def change_lesson(id, request_json):
    try:
        lesson = Lesson.query.filter(Lesson.id == id).first()
    except Exception as e:
        return False, e
    for k, v in request_json.items():
        if hasattr(lesson, k):
            setattr(lesson, k, v)
    db.session.add(lesson)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def find_terms(condition):
    try:
        terms = Term.terms(condition)
    except Exception as e:
        return None, None, e
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = terms.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, None


def find_now_term():
    try:
        term = Term.query.order_by(Term.name.desc()).first()
    except Exception as e:
        return None, e
    return term, None

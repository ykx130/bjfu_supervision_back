import pymysql
from app.utils.mysql import db
from datetime import datetime, timedelta
import json
from app.utils.Error import CustomError
from app.streaming import sub_kafka
from app.core.services import form_service, notice_lesson_service
import re
import app.core.dao as dao


def lesson_week_list(lesson_week):
    lesson_weeks = list()
    lesson_week_blocks = lesson_week.replace(' ', '').split(',')
    for lesson_week_block in lesson_week_blocks:
        weeks = lesson_week_block.replace(' ', '').split('-')
        if len(weeks) == 2:
            week_begin = int(weeks[0])
            week_end = int(weeks[1])
            [lesson_weeks.append(str(week)) for week in range(week_begin, week_end + 1)]
        else:
            lesson_weeks.append(weeks[0])
    return lesson_weeks


def week_to_date(term_begin_time, week, weekday):
    time = term_begin_time
    date = time + timedelta((int(week) - 1) * 7 + int(weekday) - 1)
    return date


def update_database():
    lesson_db = pymysql.connect(host='localhost', user='root', passwd='wshwoaini', db='lessons', charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor = lesson_db.cursor()

    cursor.execute('select distinct lesson_id,lesson_attribute, lesson_state, lesson_teacher_id, lesson_name, lesson_teacher_name, \
                   lesson_semester, lesson_level, lesson_teacher_unit, lesson_unit, lesson_year, lesson_type, lesson_class, lesson_attention_reason,\
                   lesson_model, lesson_grade, assign_group from lessons')
    datas = cursor.fetchall()
    for data in datas:
        teacher_name = data['lesson_teacher_name']
        teachers = data['lesson_teacher_name'].replace(' ', '').split(',')
        data['lesson_teacher_name'] = teachers
        teacher_ids = data['lesson_teacher_id'].replace(' ', '').split(',')
        data['lesson_teacher_id'] = teacher_ids
        teacher_units = data['lesson_teacher_unit'].replace(' ', '').split(',')
        data['lesson_teacher_unit'] = teacher_units
        lesson_id = data['lesson_id']
        data['lesson_id'] = [lesson_id + teacher_id for teacher_id in teacher_ids]
        term_name = '-'.join([data['lesson_year'], data['lesson_semester']]).replace(' ', '')
        term, err = dao.Term.get_term(term_name=term_name)
        if err is not None:
            continue
        if term is None:
            continue
        term_begin_time = term.begin_time
        for index in range(len(teachers)):
            lesson = Lesson()
            lesson.term = term_name
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
            cursor.execute('select lesson_week, lesson_time, lesson_weekday, lesson_room from lessons where lesson_id \
                            ='{}' and lesson_teacher_name='{}''.format(lesson_id, teacher_name))
            lesson_case_datas = cursor.fetchall()
            lesson_time_map = {'01': '0102', '02': '0102', '03': '0304', '04': '0304', '05': '05',
                               '06': '0607',
                               '07': '0607', '08': '0809', '09': '0809', '10': '1011', '11': '1011',
                               '12': '12'}
            for lesson_case_data in lesson_case_datas:
                if lesson_case_data['lesson_week'] == '':
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
                else:
                    weeks = lesson_week_list(lesson_case_data['lesson_week'])
                    for week in weeks:
                        lesson_time = lesson_case_data['lesson_time']
                        lesson_time_set = set()
                        lesson_times_beg = re.findall(r'.{2}', lesson_time)
                        for lesson_time_beg in lesson_times_beg:
                            lesson_time_set.add(lesson_time_map[lesson_time_beg])
                        for lesson_time in lesson_time_set:
                            lesson_case = LessonCase()
                            for k, v in lesson_case_data.items():
                                try:
                                    v = json.loads(v)
                                except:
                                    v = v
                                if v is None or v is '':
                                    continue
                                if k == 'lesson_week':
                                    lesson_case.lesson_week = week
                                    continue
                                if k == 'lesson_time':
                                    lesson_case.lesson_time = lesson_time
                                    continue
                                if hasattr(lesson_case, k):
                                    setattr(lesson_case, k, v)
                            date = week_to_date(term_begin_time, week, lesson_case.lesson_weekday)
                            lesson_case.lesson_date = date
                            lesson_case.lesson_id = lesson.id
                            db.session.add(lesson_case)
                            db.session.commit()


def lesson_to_model(lesson):
    try:
        lesson_cases = [{'lesson_week': lesson_case.lesson_week, 'lesson_time': str(lesson_case.lesson_time),
                         'lesson_date': str(lesson_case.lesson_date.strftime('%Y-%m-%d')),
                         'lesson_weekday': lesson_case.lesson_weekday,
                         'lesson_room': lesson_case.lesson_room} for
                        lesson_case in lesson.lesson_cases]
        lesson_model = {'id': lesson.id, 'lesson_id': lesson.lesson_id, 'lesson_attribute': lesson.lesson_attribute,
                        'lesson_state': lesson.lesson_state, 'lesson_teacher_id': lesson.lesson_teacher_id,
                        'lesson_name': lesson.lesson_name, 'lesson_teacher_name': lesson.lesson_teacher_name,
                        'lesson_semester': lesson.lesson_semester, 'lesson_level': lesson.lesson_level,
                        'lesson_teacher_unit': lesson.lesson_teacher_unit, 'lesson_unit': lesson.lesson_unit,
                        'lesson_year': lesson.lesson_year, 'lesson_type': lesson.lesson_type,
                        'lesson_class': lesson.lesson_class, 'lesson_grade': lesson.lesson_grade,
                        'lesson_cases': lesson_cases, 'lesson_model': lesson.lesson_model,
                        'term': lesson.term}
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return lesson_model, None


def find_lesson(lesson_id):
    try:
        lesson = Lesson.query.filter(Lesson.lesson_id == lesson_id).filter(Lesson.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if lesson is None:
        return None, CustomError(404, 404, 'lesson not found')
    return lesson, None


def has_lesson(id):
    try:
        lesson = Lesson.query.filter(Lesson.lesson_id == id).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return False, None if lesson is None else True, None


def find_lessons(condition):
    try:
        lessons = Lesson.lessons(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = condition['_page'][0] if '_page' in condition else 1
    per_page = condition['_per_page'][0] if '_per_page' in condition else 20
    pagination = lessons.paginate(page=int(page), per_page=int(per_page), error_out=False)
    lesson_page = pagination.items
    return lesson_page, pagination.total, None


def change_lesson(id, request_json):
    try:
        lesson = Lesson.query.filter(Lesson.id == id).filter(Lesson.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if lesson is None:
        return False, CustomError(404, 404, 'lesson not found')
    for k, v in request_json.items():
        if hasattr(lesson, k):
            setattr(lesson, k, v)
    db.session.add(lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_lesson_notices(lesson_id):
    try:
        lesson = Lesson.query.filter(Lesson.lesson_id == lesson_id).filter(Lesson.using == True).first()
    except Exception as e:
        raise e
    (notice_num, err) = form_service.lesson_forms_num(lesson_id)
    if err is not None:
        raise err
    lesson.notices = notice_num
    db.session.add(lesson)
    try:
        db.session.commit()
    except Exception as e:
        raise e


@sub_kafka('lesson_service')
def lesson_service_server(message):
    method = message.get('method')
    if not method:
        return
    if method == 'add_notice_lesson' or method == 'delete_notice_lesson':
        notice_lesson_service.update_page_data()


@sub_kafka('form_service')
def lesson_form_service_server(message):
    method = message.get('method')
    if not method:
        return
    if method == 'add_form' or method == 'repulse_form':
        update_lesson_notices(message.get('args', {}).get('lesson_id', None))

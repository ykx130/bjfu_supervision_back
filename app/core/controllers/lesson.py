import app.core.dao as dao
from app.utils import CustomError, db
from app.streaming import send_kafka_message
from app.utils.Error import CustomError
import pandas
import datetime
from datetime import datetime, timedelta
import pymysql
import json
import re


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


class LessonController(object):
    @classmethod
    def formatter(cls, lesson: dict = {}):
        lesson_id = lesson.get('id', 0)
        lesson_cases = dao.LessonCase.query_lesson_cases(query_dict={'lesson_id': [lesson_id], '_per_page': [100000]},
                                                         unscoped=False)
        lesson['lesson_cases'] = lesson_cases
        return lesson

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def update_database(cls, ctx: bool = True, info: dict = {}):
        host = info.get("host", "localhost")
        user = info.get("user", "root")
        passwd = info.get("passwd", "wshwoaini")
        database = info.get("db", "lesson")
        charset = info.get("charset", "utf8")
        try:
            lesson_db = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset=charset,
                                        cursorclass=pymysql.cursors.DictCursor)
            cursor = lesson_db.cursor()

            cursor.execute('select distinct lesson_id,lesson_attribute, lesson_state, lesson_teacher_id, lesson_name, lesson_teacher_name, \
                           lesson_semester, lesson_level, lesson_teacher_unit, lesson_unit, lesson_year, lesson_type, lesson_class, lesson_attention_reason,\
                           lesson_model, lesson_grade, assign_group from lessons')
            datas = cursor.fetchall()
        except Exception as e:
            raise CustomError(500, 500, str(e))
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
            try:
                for index in range(len(teachers)):
                    lesson_id = data['lesson_id'][index]
                lesson_data = dict()
                lesson_data['term'] = term_name
                for k, v in data.items():
                    try:
                        v = json.loads(v)
                    except:
                        v = v
                    if v is None or v is '':
                        continue
                    if type(v) is list:
                        lesson_data[k] = v[index]
                    else:
                        lesson_data[k] = v
                dao.Lesson.insert_lesson(ctx=False, data=lesson_data)
                cursor.execute("select lesson_week, lesson_time, lesson_weekday, lesson_room from lessons where lesson_id \
                                            ='{}' and lesson_teacher_name='{}'".format(lesson_id, teacher_name))
                lesson_cases = cursor.fetchall()
                lesson_time_map = {'01': '0102', '02': '0102', '03': '0304', '04': '0304', '05': '05',
                                   '06': '0607',
                                   '07': '0607', '08': '0809', '09': '0809', '10': '1011', '11': '1011',
                                   '12': '12'}
                for lesson_case in lesson_cases:
                    if lesson_case['lesson_week'] == '':
                        lesson_case_data = {'lesson_id': lesson_id}
                        for k, v in lesson_case.items():
                            try:
                                v = json.loads(v)
                            except:
                                v = v
                            if v is None or v is '':
                                continue
                            lesson_case_data[k] = v
                        dao.LessonCase.insert_lesson_case(ctx=False, data=lesson_case_data)
                    else:
                        weeks = lesson_week_list(lesson_case['lesson_week'])
                        for week in weeks:
                            lesson_time = lesson_case['lesson_time']
                            lesson_time_set = set()
                            lesson_times_beg = re.findall(r'.{2}', lesson_time)
                            for lesson_time_beg in lesson_times_beg:
                                lesson_time_set.add(lesson_time_map[lesson_time_beg])
                            for lesson_time in lesson_time_set:
                                lesson_case_data = {'lesson_id': lesson_id}
                                for k, v in lesson_case.items():
                                    try:
                                        v = json.loads(v)
                                    except:
                                        v = v
                                    if v is None or v is '':
                                        continue
                                    if k == 'lesson_week':
                                        lesson_case_data['lesson_week'] = week
                                        continue
                                    if k == 'lesson_time':
                                        lesson_case_data['lesson_time'] = lesson_time
                                        continue
                                    lesson_case_data[k] = v
                                    dao.LessonCase.insert_lesson_case(ctx=False, data=lesson_case_data)
                                date = week_to_date(term_begin_time, week, lesson_case.lesson_weekday)
                                lesson_case_data['lesson_date'] = date
                if ctx:
                    db.session.commit()
            except Exception as e:
                if ctx:
                    db.session.rollback()
                if isinstance(e, CustomError):
                    raise e
                else:
                    raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_lesson(cls, id: int, unscoped: bool = False):
        lesson = dao.Lesson.get_lesson(id=id, unscoped=unscoped)
        return cls.formatter(lesson)

    @classmethod
    def query_lessons(cls, query_dict: dict = {}, unscoped: bool = False):
        query_dict = cls.reformatter_insert(query_dict)
        (lessons, num) = dao.Lesson.query_lessons(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(lesson) for lesson in lessons], num

    @classmethod
    def update_lesson(cls, ctx: bool = True, id: int = 0, data: dict = {}):
        dao.Lesson.get_lesson(id=id, unscoped=False)
        try:
            dao.Lesson.update_lesson(ctx=ctx, query_dict={'id': [id]}, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True


class TermController(object):
    @classmethod
    def formatter(cls, term: dict):
        return term

    @classmethod
    def reformatter(cls, data: dict):
        return data

    @classmethod
    def get_term(cls, term_name: str, unscoped=False):
        term = dao.Term.get_term(term_name=term_name, unscoped=unscoped)
        return cls.formatter(term)

    @classmethod
    def query_terms(cls, query_dict: dict = {}, unscoped=False):
        (terms, num) = dao.Term.query_terms(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(term) for term in terms], num

    @classmethod
    def get_now_term(cls):
        term = dao.Term.get_now_term()
        return cls.formatter(term)

import app.core.dao as dao
import pymysql
from app.utils.misc import convert_string_to_datetime
from app.utils.Error import CustomError
import json
from datetime import datetime, timedelta
import re
from app import app

ctx = app.app_context()
ctx.push()


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
    time = convert_string_to_datetime(term_begin_time)
    date = time + timedelta((int(week) - 1) * 7 + int(weekday) - 1)
    return date


def update_database(info: dict = None):
    if info is None:
        info = {}
    host = info.get("host", "localhost")
    user = info.get("user", "root")
    passwd = info.get("passwd", "wshwoaini")
    database = info.get("db", "lessons")
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
        if '补考' in data['lesson_class']:
            continue
        teacher_name = data['lesson_teacher_name']
        teachers = data['lesson_teacher_name'].replace(' ', '').split(',')
        data['lesson_teacher_name'] = teachers
        teacher_ids = data['lesson_teacher_id'].replace(' ', '').split(',')
        data['lesson_teacher_id'] = teacher_ids
        teacher_units = data['lesson_teacher_unit'].replace(' ', '').split(',')
        data['lesson_teacher_unit'] = teacher_units
        lesson_id = data['lesson_id']
        data['raw_lesson_id'] = lesson_id
        term_name = '-'.join([data['lesson_year'], data['lesson_semester']]).replace(' ', '')
        term = dao.Term.get_term(term_name=term_name)
        data['lesson_id'] = [lesson_id + teacher_id + term_name.replace('-', '') for teacher_id in teacher_ids]
        if term is None:
            parts = term_name.split('-')
            if int(parts[2]) == 1:
                begin_year = parts[0]
                end_year = parts[1]
                begin_time = begin_year + '-09-01'
                end_time = end_year + '-02-14'
            else:
                begin_year = parts[1]
                end_year = parts[1]
                begin_time = begin_year + '-02-14'
                end_time = end_year + '-09-01'
            term_data = {'name': term_name, 'begin_time': begin_time, 'end_time': end_time}
            dao.Term.insert_term(ctx=True, data=term_data)
            term = dao.Term.get_term(term_name=term_name)
        term_begin_time = term['begin_time']

        for index in range(len(teachers)):
            new_lesson_id = data['lesson_id'][index]
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
            dao.Lesson.insert_lesson(ctx=True, data=lesson_data)
            new_lesson = dao.Lesson.get_lesson(lesson_id=new_lesson_id)
            cursor.execute("select lesson_week, lesson_time, lesson_weekday, lesson_room from lessons where lesson_id \
                                        ='{}' and lesson_teacher_name='{}'".format(lesson_id, teacher_name))
            lesson_cases = cursor.fetchall()
            lesson_time_map = {'01': '0102', '02': '0102', '03': '0304', '04': '0304', '05': '05',
                               '06': '0607',
                               '07': '0607', '08': '0809', '09': '0809', '10': '1011', '11': '1011',
                               '12': '12'}
            for lesson_case in lesson_cases:
                if lesson_case['lesson_week'] == '':
                    lesson_case_data = {'lesson_id': new_lesson['id']}
                    for k, v in lesson_case.items():
                        try:
                            v = json.loads(v)
                        except:
                            v = v
                        if v is None or v is '':
                            continue
                        lesson_case_data[k] = v
                    dao.LessonCase.insert_lesson_case(ctx=True, data=lesson_case_data)
                else:
                    weeks = lesson_week_list(lesson_case['lesson_week'])
                    for week in weeks:
                        lesson_time = lesson_case['lesson_time']
                        lesson_time_set = set()
                        lesson_times_beg = re.findall(r'.{2}', lesson_time)
                        for lesson_time_beg in lesson_times_beg:
                            lesson_time_set.add(lesson_time_map[lesson_time_beg])
                        for lesson_time in lesson_time_set:
                            lesson_case_data = {'lesson_id': new_lesson['id']}
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
                            date = week_to_date(term_begin_time, week, lesson_case_data['lesson_weekday'])
                            lesson_case_data['lesson_date'] = date
                            dao.LessonCase.insert_lesson_case(ctx=True, data=lesson_case_data)
    return True

if __name__ == '__main__':
    update_database()
import app.core.dao as dao
from app.utils import CustomError, db
from app.streaming import send_kafka_message
from app.utils.Error import CustomError
import pandas
import datetime
from datetime import datetime, timedelta
import pymysql



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
    def formatter(cls, model_lesson):
        lesson = dao.Lesson.get_lesson(id=model_lesson.get('lesson_id', 0), unscoped=True)
        lesson_keys = ['lesson_attribute', 'lesson_state', 'lesson_level', 'lesson_model', 'lesson_name',
                       'lesson_teacher_id', 'notices', 'term']
        for lesson_key in lesson_keys:
            model_lesson[lesson_key] = lesson.get(lesson_key, '')
        return model_lesson

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data


    @classmethod
    def update_database(cls, ctx:bool=True):
        try:
            lesson_db = pymysql.connect(host='localhost', user='root', passwd='wshwoaini', db='lessons', charset='utf8',
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
                cursor.execute("select lesson_week, lesson_time, lesson_weekday, lesson_room from lessons where lesson_id \
                                            ='{}' and lesson_teacher_name='{}'".format(lesson_id, teacher_name))
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
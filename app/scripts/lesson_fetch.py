'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-10-03 21:09:28
@LastEditTime: 2019-11-22 11:40:35
@LastEditors: Please set LastEditors
'''
import app.core.dao as dao
import pymysql
from app.utils.misc import convert_string_to_datetime, convert_datetime_to_string
from app.utils.Error import CustomError
import app.core.services as service
import json
from datetime import datetime, timedelta
import re
import argparse
from app import app, db as sup_db
from concurrent.futures import ThreadPoolExecutor
import hashlib

ctx = app.app_context()
ctx.push()

def get_md5(raw):
    """
    获取raw的md5
    :param raw:
    :return:
    """
    m2 = hashlib.md5()
    m2.update(raw)
    return m2.hexdigest()


def lesson_id_gen(raw_lesson_id, term, lesson_teacher_id):
    """
    得到md5格式的值
    """
    return get_md5(str(raw_lesson_id + term + lesson_teacher_id ).encode('utf-8'))

def lesson_week_list(lesson_week):
    """
    得到课程上课的周次

    """
    lesson_weeks = list()
    lesson_week_blocks = lesson_week.replace(' ', '').split(',')
    for lesson_week_block in lesson_week_blocks:
        if lesson_week_block == '':
            continue
        weeks = lesson_week_block.replace(' ', '').split('-')
        if len(weeks) == 2:
            week_begin = int(weeks[0])
            week_end = int(weeks[1])
            [lesson_weeks.append(str(week))
             for week in range(week_begin, week_end + 1)]
        else:
            lesson_weeks.append(weeks[0])
    return lesson_weeks


def week_to_date(term_begin_time, week, weekday):
    """
    根据学期开始时间，周次，星期几计算日期
    """
    time = convert_string_to_datetime(term_begin_time)
    date = time + timedelta((int(week) - 1) * 7 + int(weekday))
    return date.date()


def get_cursor(info: dict):
    """
    连接数据库
    """
    if info is None:
        info = {}
    host = info.get("host", "localhost")
    user = info.get("user", "root")
    passwd = info.get("passwd", "Root!!2018")
    database = info.get("db", "raw_supervision")
    charset = info.get("charset", "utf8")
    lesson_db = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset=charset,
                                cursorclass=pymysql.cursors.DictCursor)
    cursor = lesson_db.cursor()
    return cursor


def query_raw_lessons(cursor, term=None):
    """

    从数据库取出所需学期的课程并判断学期格式是否正确
    """
    sql = "select distinct lesson_id,lesson_attribute, lesson_state, lesson_teacher_id, lesson_name, lesson_teacher_name,\
         lesson_semester, lesson_level, lesson_teacher_unit, lesson_unit, lesson_year, lesson_type, lesson_class,\
          lesson_grade, lesson_week, lesson_weekday, lesson_room from origin_lessons"
    if term is not None:
        parts = term.split('-')
        if len(parts) != 3:
            raise CustomError(500, 200, 'term format is wrong')
        lesson_year = '-'.join(parts[0:2])
        lesson_semester = parts[2]
        #过滤当前学期与与课程开课学期相符的课程
        filter_sql = "where lesson_year= '{lesson_year}'and lesson_semester = '{lesson_semester}'".format(
            lesson_year=lesson_year, lesson_semester=lesson_semester)
        sql = " ".join([sql, filter_sql])
    cursor.execute(sql)
    datas = cursor.fetchall()
    return datas


def format_raw_lesson(data):
    """

    将教务处课程数据格式进行处理改为督导系统格式
    """
    teachers = data['lesson_teacher_name'].replace(' ', '').split(',')
    data['lesson_raw_teacher_name'] = data['lesson_teacher_name']
    data['lesson_teacher_name'] = teachers
    teacher_ids = data['lesson_teacher_id'].replace(' ', '').split(',')
    data['lesson_teacher_id'] = teacher_ids
    teacher_units = data['lesson_teacher_unit'].replace(' ', '').split(',')
    data['lesson_teacher_unit'] = teacher_units
    lesson_id = data['lesson_id']
    data['raw_lesson_id'] = lesson_id

    term_name = '-'.join([data['lesson_year'],
                          str(data['lesson_semester'])]).replace(' ', '')
    #lesson_id为教师、课程id和学期信息的集合
    data['lesson_id'] = [lesson_id_gen(
        raw_lesson_id=lesson_id,
        term=term_name,
        lesson_teacher_id=teacher_id
    ) for teacher_id in teacher_ids]

    lesson_datas = list()
    for index in range(len(teachers)):
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
        lesson_datas.append(lesson_data)
    return lesson_datas


def update_lesson(query_dict: dict, data: dict):
    """

    更新课程
    """
    not_allow_column = ['lesson_model',
                        'notices', 'lesson_level', 'lesson_state']
    new_data = dict()
    for key, value in data.items():
        if key not in not_allow_column:
            new_data[key] = value
    dao.Lesson.update_lesson(query_dict=query_dict, data=data)


def insert_term(term_name):
    """

    插入学期
    """
    parts = term_name.split('-')
    if int(parts[2]) == 1:
        begin_year = parts[0]
        end_year = parts[1]
        begin_time = begin_year + '-09-01'
        end_time = end_year + '-02-14'
    else:
        begin_year = parts[1]
        end_year = parts[1]
        begin_time = end_year + '-02-14'
        end_time = str(int(end_year)+1) + '-09-01'
    term_data = {'name': term_name,
                 'begin_time': begin_time, 'end_time': end_time}
    dao.Term.insert_term(ctx=True, data=term_data)
    term = dao.Term.get_term(term_name=term_name)
    return term


def query_raw_lesson_cases(cursor, lesson_id, teacher_name, lesson_year, lesson_semester):
    """

    从数据库取出教务处中开课学期 教师姓名及id并格式化
    """
    cursor.execute("select lesson_id,lesson_attribute, lesson_state, lesson_teacher_id, lesson_name, lesson_teacher_name,\
         lesson_semester, lesson_level, lesson_teacher_unit, lesson_unit, lesson_year, lesson_type, lesson_class,\
          lesson_grade, lesson_week, lesson_weekday, lesson_room, lesson_time from origin_lessons where lesson_id \
    ='{}' and lesson_teacher_name='{}' and lesson_year = '{}' and lesson_semester='{}'".format(
        lesson_id,
    teacher_name,
    lesson_year,
    lesson_semester
    ))
    print(lesson_id, teacher_name, lesson_year, lesson_semester)
    lesson_case_datas = cursor.fetchall()
    return lesson_case_datas


def format_raw_lesson_case(raw_lesson_case, lesson, lesson_id, term_begin_time, lesson_time_map):
    """
    处理课程具体信息（上课节次内置课程id等）

    """
    lesson_case_datas = list()
    teacher_ids = raw_lesson_case['lesson_teacher_id'].replace(' ', '').split(',')
    inner_lessson_ids = [lesson_id_gen(
        raw_lesson_id= str(lesson['raw_lesson_id']),
        term= lesson['term'],
        lesson_teacher_id=teacher_id
    ) for teacher_id in teacher_ids]
    inner_lesson_id = inner_lessson_ids[0]
    if lesson['lesson_id'] in inner_lessson_ids:
        inner_lesson_id = lesson['lesson_id']
    if raw_lesson_case['lesson_week'] == '':
        lesson_case_data = {'lesson_id': lesson_id, 'inner_lesson_id': inner_lesson_id}
        for k, v in raw_lesson_case.items():
            if k not in lesson_case_data:
                try:
                    v = json.loads(v)
                except:
                    v = v
                if v is None or v is '':
                    continue
                lesson_case_data[k] = v
        lesson_case_datas.append(lesson_case_data)
    else:
        weeks = lesson_week_list(raw_lesson_case['lesson_week'])
        for week in weeks:
            lesson_time = raw_lesson_case['lesson_time']
            lesson_time_set = set()
            lesson_times_beg = re.findall(r'.{2}', lesson_time)
            for lesson_time_beg in lesson_times_beg:
                lesson_time_set.add(lesson_time_map.get(lesson_time_beg, '14'))
            for lesson_time in lesson_time_set:
                lesson_case_data = {'lesson_id': lesson_id, 'inner_lesson_id': inner_lesson_id}
                for k, v in raw_lesson_case.items():
                    if k not in lesson_case_data:
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
                date = week_to_date(term_begin_time, week,
                                    lesson_case_data['lesson_weekday'])
                lesson_case_data['lesson_date'] = date
                lesson_case_datas.append(lesson_case_data)
    return lesson_case_datas


def insert_lesson(data: dict):
    dao.Lesson.insert_lesson(data=data)
    lesson = dao.Lesson.get_lesson(query_dict={'lesson_id': data['lesson_id']})
    return lesson


def insert_lesson_case(data: dict):
    """

    向数据库添加课程具体信息
    """
   
    data['term']=data['lesson_year'].replace('-','_')+'_'+str(data['lesson_semester']) 
    dao.LessonCase.get_table(term=data['term']).insert_lesson_case(data=data)
    

def del_lesson_cases(query_dict: dict):
    dao.LessonCase.get_table(term=query_dict['term']).delete_lesson_case(query_dict=query_dict)


def if_has_lesson(query_dict: dict):
    """

    判断课程是否存在
    """

    lesson = dao.Lesson.get_lesson(query_dict=query_dict)
    return lesson

def update_database(info: dict = None):
    """
    更新数据库
    """
    # lesson_time_map = {'01': '0102', '02': '0102', '03': '0304', '04': '0304', '05': '05',
    #                    '06': '0607', '07': '0607', '08': '0809', '09': '0809', '10': '10',
    #                    '11': '1112', '12': '1112', '13': '13', '14': '14'}
    lesson_time_map = {'01': '0102', '02': '0102', '03': '0304', '04': '0304', '05': '05',
                       '06': '0607', '07': '0607', '08': '0809', '09': '0809', '10': '1011',
                       '11': '1011', '12': '12', '13': '13', '14': '14'}
    cursor = get_cursor(info=info)
    term = info.get('term', None)
    raw_lessons = query_raw_lessons(cursor, term)#从数据库中过滤符合当前学期的课程 
    dao.LessonCase.get_table(term=term).query.delete()
    sup_db.session.commit()

    def update_one_lesson(raw_lesson):#更新一个课程
        if raw_lesson['lesson_teacher_name'] == '':
            return
        term_name = '-'.join([raw_lesson['lesson_year'],
                              str(raw_lesson['lesson_semester'])]).replace(' ', '')
        term = dao.Term.get_term(term_name=term_name)
        if term is None:
            term = insert_term(term_name=term_name)

        term_begin_time = term['begin_time']
        lesson_datas = format_raw_lesson(raw_lesson)#将教务处课程转化为督导课程格式

        for lesson_data in lesson_datas:
            old_lesson = if_has_lesson(query_dict={'lesson_id': [lesson_data['lesson_id']]})
            if old_lesson:
                lesson_class = old_lesson['lesson_class'] 
                print(11,lesson_data['lesson_class'])
                print(44,old_lesson['lesson_class'])
                if lesson_data['lesson_class'] not in old_lesson['lesson_class'] and len(
                        old_lesson['lesson_class']) < 100:
                        lesson_class = lesson_class +','+ lesson_data['lesson_class']
                        print(55,lesson_class)    
                update_lesson(query_dict={'lesson_id': [lesson_data['lesson_id']]}, data={
                    'lesson_class' : lesson_class,
                })
            else:
                dao.Lesson.insert_lesson(ctx=True, data=lesson_data)
            new_lesson = dao.Lesson.get_lesson(
                query_dict={'lesson_id': lesson_data['lesson_id']})
            del_lesson_cases(query_dict={'lesson_id': [new_lesson['id']], 'term':term['name']})
            raw_lesson_case_datas = query_raw_lesson_cases(cursor=cursor, lesson_id=lesson_data['raw_lesson_id'],
                                                           teacher_name=lesson_data['lesson_raw_teacher_name'],
                                                           lesson_year=raw_lesson['lesson_year'],
                                                           lesson_semester=str(raw_lesson['lesson_semester']))
            for raw_lesson_case_data in raw_lesson_case_datas:
                if raw_lesson_case_data['lesson_week'] == '' or raw_lesson_case_data['lesson_weekday'] == '':
                    continue
                lesson_case_datas = format_raw_lesson_case(raw_lesson_case=raw_lesson_case_data,
                                                           lesson=new_lesson,
                                                           lesson_id=new_lesson['id'], term_begin_time=term_begin_time,
                                                           lesson_time_map=lesson_time_map)
                for lesson_case_data in lesson_case_datas:
                    insert_lesson_case(data=lesson_case_data)
    for raw_lesson in raw_lessons:
        update_one_lesson(raw_lesson)

    return True

def run():
    """
    设置默认参数

    """
    # 创建解析器
    parser = argparse.ArgumentParser()
    #添加参数
    parser.add_argument('--term', '-t', help='请输入学期', default='2021-2022-1')
    parser.add_argument('--host', '-H', help='请输入主机名', default='localhost')
    parser.add_argument('--user', '-u', help='请输入用户名', default='root')
    parser.add_argument('--passwd', '-p', help='请输入密码', default='Root!!2018')
    parser.add_argument('--db', '-d', help='请输入数据库名', default='supervision')
    parser.add_argument('--charset', '-c', help='请输入编码格式', default='utf8')
    #解析参数
    args = parser.parse_args()
    info = {'term': args.term, 'host': args.host, 'user': args.user, 'passwd': args.passwd, 'db': args.db,
            'charset': args.charset}
    #格式化参数
    print('begin {}'.format(info))
    #更新数据库
    update_database(info=info)


if __name__ == '__main__':
    run()

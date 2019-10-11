import app.core.dao as dao
import cx_Oracle
import argparse
from app import app
import os
from datetime import datetime

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

ctx = app.app_context()
ctx.push()


def get_cursor(info: dict):
    if info is None:
        info = {}
    host = info.get("host", "202.204.121.76")
    user = info.get("user", "bjlydx_pj")
    passwd = info.get("passwd", "bjlydx_pj")
    database = info.get("db", "orcl")

    conn = cx_Oracle.connect('{}/{}@{}:1521/{}'.format(user, passwd, host, database))
    cursor = conn.cursor()
    return cursor


def crawl(cursor, page, per_page, info):
    year = info.get('year')
    semester = info.get('semester')
    begin = (page - 1) * per_page
    end = page * per_page
    cursor.execute(
        "select * from (select A.*, rownum rn from (select * from bjlydx.v_kckbsj where COURSE_YEAR='{year}' and COURSE_SEMESTER='{semester}') A where rownum <= {end}) where rn > {begin}".format(year=year, semester=semester, end=end, begin=begin))
    cols = [d[0] for d in cursor.description]
    all_data = cursor.fetchall()
    data_list = list()
    for raw_data in all_data:
        data = dict(zip(cols, raw_data))
        data_list.append(data)
    return data_list



def update_database(info=None):
    cursor = get_cursor(info)
    dao.OriginLessons.delete_all()
    per_page = info.get('per_page', 1000)
    page = 1
    crawl_info = {'year':info.get('year'), 'semester':info.get('semester')}
    while True:
        data_list = crawl(cursor, page, per_page, crawl_info)
        if not len(data_list):
            break
        print("查到课程数量: ", len(data_list))
        for data in data_list:
            print("插入 {}".format(data))
            lesson_weekday = None
            lesson_time = None
            if data['COURSE_TIME'] is not None:
                lesson_weekday = data['COURSE_TIME'][0]
                lesson_time = data['COURSE_TIME'][1:]
            insert_data = {'lesson_id': data['COURSE_ID'], 'lesson_attribute': data['COURSE_ATTRIBUTE'],
                           'lesson_state': '未完成', 'lesson_level': '自主听课', 'lesson_name': data['COURSE_NAME'],
                           'lesson_teacher_id': data['COURSE_TEACHER_ID'],
                           'lesson_teacher_name': data['COURSE_TEACHER_NAME'],
                           'lesson_teacher_unit': data['COURSE_TEACHER_UNIT'], 'lesson_unit': data['COURSE__UNIT'],
                           'lesson_year': data['COURSE_YEAR'], 'lesson_semester': data['COURSE_SEMESTER'],
                           'lesson_week': data['COURSE_WEEK'], 'lesson_weekday': lesson_weekday,
                           'lesson_time': lesson_time, 'lesson_room': data['COURSE_ROOM'],
                           'lesson_class': data['COURSE_CLASS'], 'assign_group': ''}
            dao.OriginLessons.insert(insert_data)
        page = page + 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', '-t', help='请输入学期', default='2019-2020')
    parser.add_argument('--semester', '-s', help='请输入学期', default='1')
    parser.add_argument('--host', '-H', help='请输入主机名', default='202.204.121.76')
    parser.add_argument('--user', '-u', help='请输入用户名', default='bjlydx_pj')
    parser.add_argument('--passwd', '-p', help='请输入密码', default='bjlydx_pj')
    parser.add_argument('--db', '-d', help='请输入数据库名', default='orcl')
    args = parser.parse_args()
    info = {'host': args.host, 'user': args.user, 'passwd': args.passwd, 'db': args.db, 'year': args.year,
            'semester': args.semester}
    print('begin {}'.format(info))
    update_database(info=info)

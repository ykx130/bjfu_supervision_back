import app.core.dao as dao
import cx_Oracle
import argparse
from app import app
import os
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


def update_database(info=None):
    cursor = get_cursor(info)
    cursor.execute('select * from bjlydx.v_kckbsj')
    cols = [d[0] for d in cursor.description]
    all_data = cursor.fetchall()
    dao.RawLesson.delete_all()
    for raw_data in all_data:
        data = dict(zip(cols, raw_data))
        lesson_weekday= None
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
                       'lesson_time': lesson_time, 'lesson_room': data['COURSE_ROOM'], 'lesson_class':data['COURSE_CLASS'], 'assign_group':''}
        dao.RawLesson.insert(insert_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', help='请输入主机名', default='202.204.121.76')
    parser.add_argument('--user', '-u', help='请输入用户名', default='bjlydx_pj')
    parser.add_argument('--passwd', '-p', help='请输入密码', default='bjlydx_pj')
    parser.add_argument('--db', '-d', help='请输入数据库名', default='orcl')
    args = parser.parse_args()
    info = {'host': args.host, 'user': args.user, 'passwd': args.passwd, 'db': args.db}
    print('begin {}'.format(info))
    update_database(info=info)


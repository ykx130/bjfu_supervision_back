import pymysql
from flask_pymongo import ObjectId
from app.core.models import Lesson, LessonCase

def update_database(mongo):
    mongo.db.lessons.drop()
    db = pymysql.connect(host="localhost",user="root",passwd="wshwoaini",db="lessons",charset='utf8',
    cursorclass = pymysql.cursors.DictCursor)

    cursor = db.cursor()

    cursor.execute("select distinct lesson_id,lesson_attribute, lesson_state, lesson_teacher_id, lesson_name, lesson_teacher_name, \
                   lesson_semester, lesson_level, lesson_teacher_unit, lesson_unit, lesson_year, lesson_type from lessons")
    i=0
    datas = cursor.fetchall()
    for data in datas:
        teacher_name = data['lesson_teacher_name']
        teachers = data['lesson_teacher_name'].replace(' ','').split(',')
        data['lesson_teacher_name'] = teachers
        teacher_ids = data['lesson_teacher_id'].replace(' ','').split(',')
        data['lesson_teacher_id'] = teacher_ids
        teacher_units = data['lesson_teacher_unit'].replace(' ','').split(',')
        data['lesson_teacher_unit'] = teacher_units
        for teacher in range(len(teachers)):

            lesson = Lesson()
            for k, v in data.items():
                if k in lesson.model:
                    if type(data[k]) is list:
                        lesson.model[k]= data[k][teacher]
                    else:
                        lesson.model[k] = v
            cursor.execute("select lesson_week, lesson_time, lesson_class, lesson_weekday, lesson_room, lesson_attention_reason, assign_group from lessons where lesson_id='{}' and lesson_teacher_name='{}'".format(data['lesson_id'], teacher_name))
            lesson_case_datas = cursor.fetchall()
            for lesson_case_data in lesson_case_datas:
                lesson_case = LessonCase()
                i+=1
                for k, v in lesson_case_data.items():
                    if k in lesson_case.model:
                        lesson_case.model[k] = v
                lesson.lesson_cases.append(lesson_case)
            lesson.lesson_case_to_dict()
            mongo.db.lessons.insert(lesson.model)
    print(i)

def find_lesson(mongo, _id):
    try:
        condition = {'_id':ObjectId(_id)}
    except:
        return None
    data = mongo.db.lessons.find_one(condition)
    return data

def find_lessons(mongo, condition=None):
    if condition is None:
        return mongo.db.lessons.find()
    if '_id' in condition:
        try:
            condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
        except:
            return None
    datas = mongo.db.lessons.find(condition)
    return datas


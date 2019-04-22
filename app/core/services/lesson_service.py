import pymysql
from app.utils.mysql import db
import json
from app.utils.Error import CustomError
from app.streaming import sub_kafka
from app.core.services import form_service, notice_lesson_service
import re
import app.core.dao as dao





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

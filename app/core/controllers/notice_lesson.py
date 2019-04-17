import app.core.dao as dao
from app.utils import CustomError, db
from app.streaming import send_kafka_message
from app.utils.Error import CustomError
import pandas
import datetime


class NoticeLessonController(object):
    @classmethod
    def formatter(cls, notice_lesson):
        lesson = dao.Lesson.get_lesson(id=notice_lesson.get('lesson_id', 0), unscoped=True)
        lesson_keys = ['lesson_attribute', 'lesson_state', 'lesson_level', 'lesson_name', 'lesson_teacher_id',
                       'notices']
        for lesson_key in lesson_keys:
            notice_lesson[lesson_key] = lesson.get(lesson_key, '')
        return notice_lesson

    @classmethod
    def reformatter_insert(cls, data: dict):
        if 'lesson_id' not in data:
            raise CustomError(500, 200, 'lesson id should be given')
        if 'assign_group' not in data:
            raise CustomError(500, 200, 'assign group should be given')
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def get_notice_lesson(cls, id: int, unscoped: bool = False):
        notice_lesson = dao.NoticeLesson.get_notice_lesson(id=id, unscoped=unscoped)
        return cls.formatter(notice_lesson)

    @classmethod
    def query_notice_lessons(cls, query_dict: dict, unscoped: bool = False):
        notice_lessons, num = dao.NoticeLesson.query_notice_lessons(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(notice_lesson) for notice_lesson in notice_lessons], num

    @classmethod
    def insert_notice_lesson(cls, ctx: bool = True, data: dict = {}):
        data['term'] = data['term'] if 'term' in data else dao.Term.get_now_term()['name']
        data = cls.reformatter_insert(data=data)
        dao.Lesson.get_lesson(id=data['lesson_id'], unscoped=False)
        try:
            dao.NoticeLesson.insert_notice_lesson(ctx=False, data=data)
            dao.Lesson.update_lesson(ctx=False, query_dict={'id': [data['lesson_id']]}, data={'lesson_level': '关注课程'})
            notice_lesson_records, num= dao.NoticeLesson.query_notice_lessons(
                query_dict={'lesson_id': [data['lesson_id']], 'term': [data['term']]}, unscoped=False)
            if num >0:
                raise CustomError(500, 200, 'lesson has been noticed')
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if type(e) == CustomError:
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

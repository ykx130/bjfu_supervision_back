import app.core.dao as dao
from app.utils import CustomError, db
from app.utils.kafka import send_kafka_message
from app.utils.Error import CustomError
import pandas
import datetime
from datetime import datetime, timedelta
import pymysql
import json
import re
import app.core.services as service
from app.utils.misc import convert_string_to_datetime


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


class LessonController(object):
    @classmethod
    def formatter(cls, lesson: dict = None):
        """
        拼接notice
        :param lesson:
        :return:
        """
        return lesson
    @classmethod
    def formater_with_level_and_model(cls, lesson:dict=None):
        if lesson['lesson_level'] == '关注课程':
            noice_lesson = dao.NoticeLesson.get_notice_lesson(query_dict={
                'lesson_id': lesson['lesson_id'],
                "term": lesson["term"]
            })
            if noice_lesson:
                lesson['group_name'] = noice_lesson['group_name']
                lesson['lesson_attention_reason'] = noice_lesson['lesson_attention_reason']
        model_lesson = dao.ModelLesson.get_model_lesson(query_dict={
            "lesson_teacher_name": lesson["lesson_teacher_name"],
            'lesson_name': lesson["lesson_name"],
            "term": lesson["term"]
        })
        print(model_lesson)
        if model_lesson:
            lesson['lesson_model'] = model_lesson['status']
            lesson['group_name'] = model_lesson['group_name']
            lesson["is_lock"] = model_lesson["is_lock"]
            lesson["guiders"] = model_lesson["guiders"]
        return lesson

    @classmethod
    def formatter_with_cases(cls, lesson: dict = None):
        (lesson_cases, _) = dao.LessonCase.get_table(term=lesson.get('term')).query_lesson_cases(query_dict={
            'inner_lesson_id': [lesson.get('lesson_id')],
            'lesson_id': [lesson.get('id')]
        }, unscoped=False)
        lesson['lesson_cases'] = lesson_cases
        return lesson
    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def update_database(cls, ctx: bool = True, info: dict = None):
        pass

    @classmethod
    def get_lesson(cls, query_dict:dict, unscoped: bool = False):
        lesson = dao.Lesson.get_lesson(query_dict=query_dict, unscoped=unscoped)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        return cls.formater_with_level_and_model(lesson)

    @classmethod
    def query_lessons(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        query_dict = cls.reformatter_insert(query_dict)
        (lessons, num) = dao.Lesson.query_lessons(query_dict=query_dict, unscoped=unscoped)
        return [cls.formater_with_level_and_model(lesson) for lesson in lessons], num

    @classmethod
    def query_lessons_with_cases(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        query_dict = cls.reformatter_insert(query_dict)
        (lessons, num) = dao.Lesson.query_lessons(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter_with_cases(lesson) for lesson in lessons], num

    @classmethod
    def update_lesson(cls, ctx: bool = True, lesson_id: str = 0, data: dict = None):
        from app.core.controller import NoticeLessonController
        if data is None:
            data = dict()
        if 'id' in data:
            del data['id']
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':lesson_id}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        lesson_level = data.get('lesson_level', None)
        if lesson_level is not None and lesson_level == '关注课程':
            notice_lesson_data = dict()
            notice_lesson_data['term'] = lesson['term']
            notice_lesson_data['group_name'] = data['group_name']
            notice_lesson_data['lesson_attention_reason'] = data['lesson_attention_reason']
            notice_lesson_data['lesson_id'] = lesson['lesson_id']
            NoticeLessonController.insert_notice_lesson(ctx=False, data=notice_lesson_data)
        try:
            dao.Lesson.update_lesson(ctx=ctx, query_dict={'lesson_id': [lesson_id]}, data=data)
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
    def query_teacher_names(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        (teacher_names, num) = dao.Lesson.query_teacher_names(query_dict=query_dict, unscoped=unscoped)
        return teacher_names, num


class LessonCaseController(object):
    @classmethod
    def formatter(self, lesson_case):
        return lesson_case

    @classmethod
    def query_lesson_cases(cls, query_dict: dict = None, unscoped: bool = False):
        print(query_dict)
      
        query_dict['_per_page'] = 10000
        (lesson_cases, num) = dao.LessonCase.get_table(term=query_dict['term'][0]).query_lesson_cases(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(lesson_case) for lesson_case in lesson_cases], num


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
        if term is None:
            raise CustomError(404, 404, 'term not found')
        return cls.formatter(term)

    @classmethod
    def query_terms(cls, query_dict: dict = None, unscoped=False):
        if query_dict is None:
            query_dict = dict()
        (terms, num) = dao.Term.query_terms(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(term) for term in terms], num

    @classmethod
    def get_now_term(cls):
        term = service.TermService.get_now_term()
        return cls.formatter(term)

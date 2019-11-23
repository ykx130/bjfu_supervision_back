import app.core.dao as dao
from app.utils import CustomError, db
from app import redis_cli
from app.utils.kafka import send_kafka_message
from app.utils.Error import CustomError
import pandas
import datetime
import json
import app.core.services as service


class LessonRecordController(object):
    @classmethod
    def formatter(cls, lesson_record):
        return lesson_record

    @classmethod
    def reformatter_insert(cls, data: dict):
        if 'username' not in data:
            raise CustomError(500, 200, 'username must be given')
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def reformatter_query(cls, data: dict):
        return data

    @classmethod
    def query_lesson_records_history(cls, query_dict: dict, unscoped: bool = False):
        (lesson_records, num) = dao.LessonRecord.query_lesson_records(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(lesson_record) for lesson_record in lesson_records], num

    @classmethod
    def query_lesson_records_term(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        if query_dict.get('term', None) is None:
            term = service.TermService.get_now_term()['name']
            query_dict.update({'term': term})
        (lesson_records, num) = dao.LessonRecord.query_lesson_records(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(lesson_record) for lesson_record in lesson_records], num

    @classmethod
    def query_lesson_record_history(cls, username: str = None, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query_dict['username'] = [username]
        (lesson_records, num) = dao.LessonRecord.query_lesson_records(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(lesson_record) for lesson_record in lesson_records], num

    @classmethod
    def get_lesson_record(cls, query_dict, unscoped: bool = False):
        if query_dict.get('term', None) is None:
            term = service.TermService.get_now_term()['name']
            query_dict.update({'term':term})
        lesson_record = dao.LessonRecord.get_lesson_record(query_dict=query_dict,
                                                           unscoped=unscoped)
        if lesson_record is None:
            raise CustomError(404, 404, 'lesson_record not found')
        return cls.formatter(lesson_record)

    @classmethod
    def delete_lesson_record(cls, ctx: bool = True, username: str = None, term: str = None):
        if term is None:
            term = service.TermService.get_now_term()['name']
        lesson_record = dao.LessonRecord.get_lesson_record(query_dict={'username': username, 'term': term},
                                                           unscoped=False)
        if lesson_record is None:
            raise CustomError(404, 404, 'lesson_record not found')
        try:
            dao.LessonRecord.delete_lesson_record(ctx=False, query_dict={'id': [lesson_record['id']]})
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
    def update_lesson_records(cls, ctx: bool = True, usernames: list = None):
        term = service.TermService.get_now_term()['name']
        try:
            for username in usernames:
                supervisor_query_dict = {'term': [term], 'username': [username]}
                user = dao.User.get_user(query_dict={'username': username}, unscoped=False)
                if user is None:
                    raise CustomError(404, 404, 'lesson_record not found')
                (supervisors, num) = dao.Supervisor.query_supervisors(query_dict=supervisor_query_dict, unscoped=False)
                for supervisor in supervisors:
                    (_, num) = dao.LessonRecord.query_lesson_records(
                        query_dict={'username': [username], 'term': [term]}, unscoped=False)
                    if num == 0:
                        data = {'term': term, 'username': username, 'group_name': supervisor['group_name'],
                                'name': user['name']}
                        dao.LessonRecord.insert_lesson_record(ctx=False, data=data)
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
    def insert_lesson_record(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        username = data.get('username', None)
        term = data.get('term', service.TermService.get_now_term()['name'])
        user = dao.User.get_user(query_dict={'username': username}, unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'lesson_record not found')
        supervisor = dao.Supervisor.get_supervisor(query_dict={'username': username, 'term': term}, unscoped=False)
        if supervisor is None:
            raise CustomError(404, 404, 'supervisor not found')
        try:
            data = {'username': username, 'term': term, 'name': user['name'], 'group_name': supervisor['group_name']}
            dao.LessonRecord.insert_lesson_record(ctx=False, data=data)
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
    def update_lesson_record(cls, ctx: bool = True, username: str = None, term: str = None, data: dict = None):
        if data is None:
            data = {}
        lesson_record = dao.LessonRecord.get_lesson_record(query_dict={'username': username, 'term': term},
                                                           unscoped=False)
        if lesson_record is None:
            raise CustomError(404, 404, 'lesson_record not found')
        try:
            dao.LessonRecord.update_lesson_record(query_dict={'id': [lesson_record['id']]}, data=data)
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
    def export_lesson_record(cls, data: dict = None):
        if data is None:
            data = dict()
        lesson_records,num=dao.LessonRecord.query_lesson_records(query_dict=data)
        column_dict={'用户工号':'username','用户姓名':'name','所在分组':'group_name',
                     '当前学期': 'term','未提交':'to_be_submitted',
                     '已提交':'has_submitted','完成总课时':'finish_total_times',
                     '只听一节课':'finish_1_times','连续完成2课时':'finish_2_times',
                     '连续完成3课时':'finish_3_times','连续完成4课时':'finish_4_times','提交总次数':'total_times'}
        frame_dict = dict()
        for lesson_record in lesson_records:
            for key, value in column_dict.items():
                excel_value = lesson_record[value] if value in lesson_record else lesson_record.get(value, "")
                if key not in frame_dict:
                    frame_dict[key] = [excel_value]
                else:
                    frame_dict[key].append(excel_value)
        try:
            frame = pandas.DataFrame(frame_dict)
            from app import basedir
            filename = '/static/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            fullname = basedir + filename
            frame.to_excel(fullname, sheet_name='123', index=False, header=True)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return filename

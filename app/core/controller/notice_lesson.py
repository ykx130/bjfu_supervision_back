import app.core.dao as dao
from app.utils import CustomError, db
from app import redis_cli
from app.utils.kafka import send_kafka_message
from app.utils.Error import CustomError
import pandas
import datetime
import app.core.services as service
import json


class NoticeLessonController(object):
    @classmethod
    def formatter(cls, notice_lesson):
        lesson = dao.Lesson.get_lesson(query_dict={
            'lesson_id':notice_lesson.get('lesson_id', 0),
        }, unscoped=True)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        lesson_keys = ['lesson_attribute', 'lesson_state', 'lesson_level', 'lesson_model', 'lesson_name',
                       'lesson_teacher_id', 'notices', 'term', 'lesson_class', 'lesson_unit', 'lesson_teacher_name']
        for lesson_key in lesson_keys:
            notice_lesson[lesson_key] = lesson.get(lesson_key, '')
        return notice_lesson

    @classmethod
    def reformatter_insert(cls, data: dict):
        if 'lesson_id' not in data:
            raise CustomError(500, 200, 'lesson id should be given')
        if 'group_name' not in data:
            raise CustomError(500, 200, 'group name should be given')
        if 'lesson_attention_reason' not in data:
            raise CustomError(500, 200, 'notice reason should be given')
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def reformatter_query(cls, data: dict):
        return data

    @classmethod
    def get_notice_lesson(cls, query_dict:dict, unscoped: bool = False):
        notice_lesson = dao.NoticeLesson.get_notice_lesson(query_dict=query_dict, unscoped=unscoped)
        if notice_lesson is None:
            raise CustomError(404, 404, 'notice_lesson not found')
        return cls.formatter(notice_lesson)

    @classmethod
    def query_notice_lessons(cls, query_dict: dict, unscoped: bool = False):
        (notice_lessons, num) = dao.NoticeLesson.query_notice_lessons(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(notice_lesson) for notice_lesson in notice_lessons], num

    @classmethod
    def insert_notice_lesson(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        data['term'] = data.get('term', service.TermService.get_now_term()['name'])
        data = cls.reformatter_insert(data=data)
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':data['lesson_id']}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        try:
            (notice_lesson_records, num) = dao.NoticeLesson.query_notice_lessons(
                query_dict={'lesson_id': [data['lesson_id']], 'term': [data['term']]}, unscoped=False)
            if num > 0:
                raise CustomError(500, 200, 'lesson has been noticed')
            dao.NoticeLesson.insert_notice_lesson(ctx=False, data=data)
            dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [data['lesson_id']]},
                                     data={'lesson_level': '关注课程'})
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
    def insert_notice_lessons(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        data['term'] = data.get('term', service.TermService.get_now_term()['name'])
        lesson_ids = data.get('lesson_ids', [])
        try:
            for lesson_id in lesson_ids:
                lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':lesson_id}, unscoped=False)
                if lesson is None:
                    raise CustomError(404, 404, 'lesson not found')
                (_, num) = dao.NoticeLesson.query_notice_lessons(query_dict={'lesson_id': [lesson_id]}, unscoped=False)
                if num != 0:
                    continue
                data['lesson_id'] = lesson_id
                data = cls.reformatter_insert(data)
                dao.NoticeLesson.insert_notice_lesson(ctx=False, data=data)
                dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [lesson_id]},
                                         data={'lesson_level': '关注课程'})
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
    def update_page_data(cls, term: str = None, unscoped=False):
        if term is None:
            term = service.TermService.get_now_term()['name']
        (_, num) = dao.NoticeLesson.query_notice_lessons(query_dict={'term': [term]}, unscoped=False)
        try:
            redis_cli.set('sys:notice_lesson_num', json.dumps(num))
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return num

    @classmethod
    def update_notice_lesson(cls, ctx: bool = True, id: int = 0, data: dict = None):
        if data is None:
            data = dict()
        notice_lesson = dao.NoticeLesson.get_notice_lesson(query_dict={'id':id}, unscoped=False)
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':notice_lesson['lesson_id']}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        try:
            dao.NoticeLesson.update_notice_lesson(ctx=False, query_dict={'id': [id]}, data=data)
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
    def delete_notice_lesson(cls, ctx: bool = True, id: int = 0):
        notice_lesson = dao.NoticeLesson.get_notice_lesson(query_dict={'id':id}, unscoped=False)
        if notice_lesson is None:
            raise CustomError(404, 404, 'notice_lesson not found')
        try:
            lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':notice_lesson['lesson_id']}, unscoped=False)
            if lesson is None:
                raise CustomError(404, 404, 'lesson not found')
            dao.NoticeLesson.delete_notice_lesson(ctx=False, query_dict={'id': [id]})
            dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [notice_lesson['lesson_id']]},
                                     data={'lesson_level': '自主听课'})
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
    def delete_notice_lessons(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        notice_lesson_ids = data.get('notice_lesson_ids', [])
        try:
            for notice_lesson_id in notice_lesson_ids:
                notice_lesson = dao.NoticeLesson.get_notice_lesson(query_dict={'id':notice_lesson_id}, unscoped=False)
                if notice_lesson is None:
                    raise CustomError(404, 404, 'notice_lesson not found')
                lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':notice_lesson['lesson_id']}, unscoped=False)
                if lesson is None:
                    raise CustomError(404, 404, 'lesson not found')
                dao.NoticeLesson.delete_notice_lesson(ctx=False, query_dict={'id': [notice_lesson_id]})
                dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [notice_lesson['lesson_id']]},
                                         data={'lesson_level': '自助听课'})
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
    def notice_lesson_vote(cls, ctx: bool = True, id: int = 0):
        notice_lesson = dao.NoticeLesson.get_notice_lesson(query_dict={'id':id}, unscoped=False)
        if notice_lesson is None:
            raise CustomError(404, 404, 'notice_lesson not found')
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':notice_lesson['lesson_id']}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        try:
            dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': notice_lesson['lesson_id']},
                                     data={'notices': int(lesson['notices'] + 1)})
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
    def import_lesson_excel(cls, ctx: bool = True, data=None):
        if 'filename' in data.files:
            from app import basedir
            filename = basedir + '/static/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            file = data.files['filename']
            file.save(filename)
            df = pandas.read_excel(filename)
        else:
            raise CustomError(500, 200, 'file must be given')
        column_dict = {'课程名称': 'lesson_name', '课程性质': 'lesson_attribute', '学分': 'lesson_grade', '开课学年': 'lesson_year',
                       '开课学期': 'lesson_semester', '任课教师名称': 'lesson_teacher_name', '任课教师所在学院': 'lesson_teacher_unit',
                       '指定小组': 'group_name', '关注原因': 'lesson_attention_reason', '关注次数': 'notices'}
        filter_list = ['lesson_name', 'lesson_teacher_name', 'lesson_semester', 'lesson_year']
        row_num = df.shape[0]
        fail_lessons = list()
        try:
            for i in range(0, row_num):
                lesson_filter = dict()
                notice_lesson_data = dict()
                for col_name_c, col_name_e in column_dict.items():
                    notice_lesson_data[col_name_e] = str(df.iloc[i][col_name_c])
                    if col_name_e in filter_list:
                        lesson_filter[col_name_e] = [str(df.iloc[i][col_name_c])]
                (lessons, total) = dao.Lesson.query_lessons(query_dict=lesson_filter, unscoped=False)
                if total == 0:
                    fail_lessons.append(lesson_filter)
                    continue
                lesson_id = lessons[0]['lesson_id']
                term = lessons[0]['term']
                notice_lesson_data['lesson_id'] = lesson_id
                (_, num) = dao.NoticeLesson.query_notice_lessons(query_dict={'lesson_id': [lesson_id]}, unscoped=False)
                if num != 0:
                    fail_lessons.append(lesson_filter)
                    continue
                notice_lesson_data['term'] = term
                try:
                    dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [lesson_id]},
                                             data={'lesson_level': '关注课程'})
                    dao.NoticeLesson.insert_notice_lesson(ctx=False, data=notice_lesson_data)
                except:
                    fail_lessons.append(lesson_filter)
                    continue
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        file_path = None
        if len(fail_lessons) == 0:
            frame_dict = {}
            for file_lesson in fail_lessons:
                for key, value in column_dict.items():
                    if value in file_lesson:
                        excel_value = file_lesson.get(value)
                        if key not in frame_dict:
                            frame_dict[key] = [excel_value]
                        else:
                            frame_dict[key].append(excel_value)
            frame = pandas.DataFrame(frame_dict)
            from app import basedir
            filename = '/static/' + "fail" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            fullname = basedir + filename
            frame.to_excel(fullname, sheet_name='123', index=False, header=True)
        return file_path

    @classmethod
    def export_lesson_excel(cls, data: dict = None):
        if data is None:
            data = dict()
        if 'term' in data:
            notice_lessons, num = dao.NoticeLesson.query_notice_lessons(query_dict={'term': [data['term']]})
        else:
            notice_lessons, num = dao.NoticeLesson.query_notice_lessons()
        column_dict = {'课程名称': 'lesson_name', '课程性质': 'lesson_attribute', '学分': 'lesson_grade', '开课学年': 'lesson_year',
                       '开课学期': 'lesson_semester', '任课教师名称': 'lesson_teacher_name', '任课教师所在学院': 'lesson_teacher_unit',
                       '指定小组': 'group_name', '关注原因': 'lesson_attention_reason', '关注次数': 'notices'}
        frame_dict = dict()
        for notice_lesson in notice_lessons:
            lesson = dao.Lesson.get_lesson(query_dict={'lesson_id':notice_lesson['lesson_id']}, unscoped=True)
            if lesson is None:
                raise CustomError(404, 404, 'lesson not found')
            for key, value in column_dict.items():
                excel_value = lesson[value] if value in lesson else notice_lesson.get(value, "")
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

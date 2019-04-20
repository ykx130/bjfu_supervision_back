import app.core.dao as dao
from app.utils import CustomError, db
from app import redis_cli
from app.streaming import send_kafka_message
from app.utils.Error import CustomError
import pandas
import datetime
import json


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
        if 'notice_reason' not in data:
            raise CustomError(500, 200, 'notice reason should be given')
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
        (notice_lessons, num) = dao.NoticeLesson.query_notice_lessons(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(notice_lesson) for notice_lesson in notice_lessons], num

    @classmethod
    def insert_notice_lesson(cls, ctx: bool = True, data: dict = {}):
        data['term'] = data['term'] if 'term' in data else dao.Term.get_now_term()['name']
        data = cls.reformatter_insert(data=data)
        dao.Lesson.get_lesson(id=data['lesson_id'], unscoped=False)
        try:
            dao.NoticeLesson.insert_notice_lesson(ctx=False, data=data)
            dao.Lesson.update_lesson(ctx=False, query_dict={'id': [data['lesson_id']]}, data={'lesson_level': '关注课程'})
            notice_lesson_records, num = dao.NoticeLesson.query_notice_lessons(
                query_dict={'lesson_id': [data['lesson_id']], 'term': [data['term']]}, unscoped=False)
            if num > 0:
                raise CustomError(500, 200, 'lesson has been noticed')
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError) == CustomError:
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def insert_notice_lessons(cls, ctx: bool = True, data: dict = {}):
        data['term'] = data['term'] if 'term' in data else dao.Term.get_now_term()['name']
        lesson_ids = data.get('lesson_ids', [])
        try:
            for lesson_id in lesson_ids:
                dao.Lesson.get_lesson(id=lesson_id, unscoped=False)
                data['lesson_id'] = lesson_id
                data = cls.reformatter_insert(data)
                dao.NoticeLesson.insert_notice_lesson(ctx=False, data=data)
                dao.Lesson.update_lesson(ctx=False, query_dict={'id': [lesson_id]}, data={'lesson_level': '关注课程'})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError) == CustomError:
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_page_data(cls, term: str = None, unscoped=False):
        if term is None:
            term = dao.Term.get_now_term()['name']
        (_, num) = dao.NoticeLesson.query_notice_lessons(query_dict={'term': [term]}, unscoped=False)
        try:
            redis_cli.set('sys:notice_lesson_num', json.dumps(num))
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return num

    @classmethod
    def update_notice_lesson(cls, ctx: bool = True, id: int = 0, data: dict = {}):
        notice_lesson = dao.NoticeLesson.get_notice_lesson(id=id, unscoped=False)
        dao.Lesson.get_lesson(id=notice_lesson['lesson_id'], unscoped=False)
        try:
            dao.NoticeLesson.update_notice_lesson(ctx=False, query_dict={'id': [id]}, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError) == CustomError:
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_notice_lesson(cls, ctx: bool = True, id: int = 0):
        notice_lesson = dao.NoticeLesson.get_notice_lesson(id=id, unscoped=False)
        try:
            dao.Lesson.get_lesson(id=notice_lesson['lesson_id'], unscoped=False)
            dao.NoticeLesson.delete_notice_lesson(ctx=False, query_dict={'id': [id]})
            dao.Lesson.update_lesson(ctx=False, query_dict={'id': [notice_lesson['lesson_id']]},
                                     data={'lesson_level': '自主听课'})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError) == CustomError:
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_notice_lessons(cls, ctx: bool = True, data: dict = {}):
        notice_lesson_ids = data.get('notice_lesson_ids', [])
        try:
            for notice_lesson_id in notice_lesson_ids:
                notice_lesson = dao.NoticeLesson.get_notice_lesson(id=notice_lesson_id, unscoped=False)
                dao.Lesson.get_lesson(id=notice_lesson['lesson_id'], unscoped=False)
                dao.NoticeLesson.delete_notice_lesson(ctx=False, query_dict={'id': [notice_lesson_id]})
                dao.Lesson.update_lesson(ctx=False, query_dict={'id': [notice_lesson['lesson_id']]},
                                         data={'lesson_level': '自助听课'})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError) == CustomError:
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def notice_lesson_vote(cls, ctx: bool = True, id: int = 0):
        notice_lesson = dao.NoticeLesson.get_notice_lesson(id=id, unscoped=False)
        lesson = dao.Lesson.get_lesson(id=id, unscoped=False)
        try:
            dao.Lesson.update_lesson(ctx=False, query_dict={'id': notice_lesson['lesson_id']},
                                     data={'notices': int(lesson['notices'] + 1)})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError) == CustomError:
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
                       '指定小组': 'assign_group', '关注原因': 'notice_reason', '关注次数': 'notices'}
        filter_list = ['lesson_name', 'lesson_teacher_name', 'lesson_semester', 'lesson_year', 'lesson_attribute',
                       'lesson_grade']
        row_num = df.shape[0]
        try:
            for i in range(0, row_num):
                lesson_filter = dict()
                notice_lesson_data = dict()
                for col_name_c, col_name_e in column_dict.items():
                    notice_lesson_data[col_name_e] = str(df.iloc[i][col_name_c])
                    if col_name_e in filter_list:
                        lesson_filter[col_name_e] = str(df.iloc[i][col_name_c])
                lessons, total = dao.Lesson.query_lessons(query_dict=lesson_filter, unscoped=False)
                if total == 0:
                    raise CustomError(404, 404, 'lesson not found')
                lesson_id = lessons[0]['id']
                notice_lesson_data['lesson_id'] = lesson_id
                notice_lesson_data['term'] = '_'.join([str(df.iloc[i]['开课学年']), str(df.iloc[i]['开课学期'])])
                dao.NoticeLesson.insert_notice_lesson(ctx=False, data=notice_lesson_data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError) == CustomError:
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def export_lesson_excel(cls, data: dict = {}):
        if 'notice_lesson_ids' not in data:
            notice_lessons = dao.NoticeLesson.query_notice_lessons(query_dict={'_per_page': [100000]}, unscoped=False)
        else:
            notice_lesson_ids = data.get('notice_lesson_ids')
            notice_lessons = dao.NoticeLesson.query_notice_lessons(
                query_dict={'_per_page': [100000], 'id': notice_lesson_ids})
        column_dict = {'课程名称': 'lesson_name', '课程性质': 'lesson_attribute', '学分': 'lesson_grade', '开课学年': 'lesson_year',
                       '开课学期': 'lesson_semester', '任课教师名称': 'lesson_teacher_name', '任课教师所在学院': 'lesson_teacher_unit',
                       '指定小组': 'assign_group', '关注原因': 'notice_reason', '关注次数': 'notices'}
        frame_dict = dict()
        for notice_lesson in notice_lessons:
            lesson = dao.Lesson.get_lesson(id=notice_lesson['lesson_id'], unscoped=True)
            for key, value in column_dict.items():
                excel_value = lesson[value] if value in lesson else notice_lesson.get(value, "")
                if key not in frame_dict:
                    frame_dict[key] = [excel_value]
                else:
                    frame_dict[key].append(excel_value)
        try:
            frame = pandas.DataFrame(frame_dict)
            from app import basedir
            filename = basedir + '/static/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            frame.to_excel(filename, sheet_name='123', index=False, header=True)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return filename

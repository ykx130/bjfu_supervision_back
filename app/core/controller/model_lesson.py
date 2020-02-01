'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-09-30 20:45:11
@LastEditTime: 2019-11-22 16:02:29
@LastEditors: Please set LastEditors
'''
import app.core.dao as dao
from app.utils import CustomError, db
from app.utils.Error import CustomError
from flask_login import current_user
import pandas
import datetime
import app.core.services as service


class ModelLessonController(object):

    @classmethod
    def formatter(cls, model_lesson):
        lesson = dao.Lesson.get_lesson(query_dict={
            'lesson_id': model_lesson.get('lesson_id', ''),
        }, unscoped=True)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        lesson_keys = ['lesson_'
                       'attribute', 'lesson_state', 'lesson_level', 'lesson_model', 'lesson_name',
                       'lesson_teacher_id', 'notices', 'term', 'lesson_class', 'lesson_unit', 'lesson_teacher_name']
        for lesson_key in lesson_keys:
            model_lesson[lesson_key] = lesson.get(lesson_key, '')
        return model_lesson

    @classmethod
    def reformatter_insert(cls, data: dict):
        if 'lesson_id' not in data:
            raise CustomError(500, 200, 'lesson id should be given')
        data['status'] = data.get('status', '推荐为好评课')
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def reformatter_query(cls, data: dict):
        return data

    @classmethod
    def get_model_lesson(cls, query_dict: dict, unscoped: bool = False):
        model_lesson = dao.ModelLesson.get_model_lesson(query_dict=query_dict, unscoped=unscoped)
        if model_lesson is None:
            raise CustomError(404, 404, 'model_lesson not found')
        return cls.formatter(model_lesson=model_lesson)

    @classmethod
    def query_model_lessons(cls, query_dict: dict, unscoped: bool = False):
        model_lessons, num = dao.ModelLesson.query_model_lessons(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(model_lesson) for model_lesson in model_lessons], num



    @classmethod
    def insert_model_lesson(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        term = data.get('term', service.TermService.get_now_term()['name'])
        data['term'] = term
        data = cls.reformatter_insert(data=data)
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id': data['lesson_id']}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        status = data.get('status', '推荐为好评课')
        lesson_id = data.get('lesson_id', None)
        if lesson_id is None:
            raise CustomError(500, 200, 'lesson_id must be given')
        try:
            (_, num) = dao.ModelLesson.query_model_lessons(query_dict={'lesson_id': [lesson_id]}, unscoped=False)
            if num != 0:
                raise CustomError(500, 200, 'lesson has been model lesson')
            data['unit'] = lesson['lesson_unit']
            data['lesson_name'] = lesson['lesson_name']
            data['lesson_teacher_name'] = lesson['lesson_teacher_name']
            dao.ModelLesson.insert_model_lesson(ctx=False, data=data)
            dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [data['lesson_id']]},
                                     data={'lesson_model': status})
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
    def insert_model_lessons(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        lesson_ids = data.get("lesson_ids", [])
        status = data.get('status', '推荐为好评课')
        data['term'] = data.get('term', service.TermService.get_now_term()['name'])
        try:
            for lesson_id in lesson_ids:
                lesson = dao.Lesson.get_lesson(query_dict={'lesson_id': lesson_id}, unscoped=False)
                if lesson is None:
                    raise CustomError(404, 404, 'lesson not found')
                (_, num) = dao.ModelLesson.query_model_lessons(query_dict={'lesson_id': lesson_id}, unscoped=False)
                if num != 0:
                    continue
                data['lesson_id'] = lesson_id
                data['unit'] = lesson['lesson_unit']
                data['lesson_name'] = lesson['lesson_name']
                data['lesson_teacher_name'] = lesson['lesson_teacher_name']
                data = cls.reformatter_insert(data=data)
                dao.ModelLesson.insert_model_lesson(ctx=False, data=data)
                dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [lesson_id]},
                                         data={'lesson_model': status})

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
    def update_model_lesson(cls, ctx: bool = True, id: int = 0, data: dict = None):
        if data is None:
            data = dict()
        model_lesson = dao.ModelLesson.get_model_lesson(query_dict={'id': id}, unscoped=False)
        if model_lesson is None:
            raise CustomError(404, 404, 'model_lesson not found')
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id': model_lesson['lesson_id']}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        status = data.get('status', lesson['lesson_model'])
        try:
            dao.ModelLesson.update_model_lesson(ctx=False, query_dict={'id': [id]}, data=data)
            dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [model_lesson['lesson_id']]},
                                     data={'lesson_model': status})
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
    def delete_model_lesson(cls, ctx: bool = True, id: int = 0):
        model_lesson = dao.ModelLesson.get_model_lesson(query_dict={'id': id}, unscoped=False)
        if model_lesson is None:
            raise CustomError(404, 404, 'model_lesson not found')
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id': model_lesson['lesson_id']}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        try:
            dao.ModelLesson.delete_model_lesson(ctx=False, query_dict={'id': [id]})
            dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [model_lesson['lesson_id']]},
                                     data={'lesson_model': ''})
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
    def delete_model_lessons(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        model_lesson_ids = data.get('model_lesson_ids', [])
        try:
            for model_lesson_id in model_lesson_ids:
                model_lesson = dao.ModelLesson.get_model_lesson(query_dict={'id': model_lesson_id}, unscoped=False)
                if model_lesson is None:
                    raise CustomError(404, 404, 'model_lesson not found')
                lesson = dao.Lesson.get_lesson(query_dict={'lesson_id': model_lesson['lesson_id']}, unscoped=False)
                if lesson is None:
                    raise CustomError(404, 404, 'lesson not found')
                dao.ModelLesson.delete_model_lesson(ctx=False, query_dict={'id': [model_lesson_id]})
                dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [model_lesson['lesson_id']]},
                                         data={'lesson_model': ''})
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
    def model_lesson_vote(cls, ctx: bool = True, lesson_id: str = 0, vote: bool = True):
        model_lesson = dao.ModelLesson.get_model_lesson_by_lesson_id(query_dict={'lesson_id': lesson_id},
                                                                     unscoped=False)
        if model_lesson is None:
            raise CustomError(404, 404, 'model_lesson not found')
        lesson = dao.Lesson.get_lesson(query_dict={'lesson_id': model_lesson['lesson_id']}, unscoped=False)
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        try:
            if vote:
                dao.ModelLesson.update_model_lesson(ctx=False, query_dict={'lesson_id': [lesson_id]},
                                                    data={'votes': int(model_lesson['votes']) + 1})
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
        column_dict = {'课程名称': 'lesson_name', '课程性质': 'lesson_attribute', '开课学年': 'lesson_year',
                       '开课学期': 'lesson_semester', '授课教师名称': 'lesson_teacher_name', '任课教师所在学院': 'lesson_teacher_unit',
                       '听课督导组': 'group_name'}
        filter_list = ['lesson_name', 'lesson_teacher_name', 'lesson_semester', 'lesson_year']
        row_num = df.shape[0]
        fail_lessons = list()
        try:
            for i in range(0, row_num):
                lesson_filter = dict()
                model_lesson_data = dict()
                for col_name_c, col_name_e in column_dict.items():
                    model_lesson_data[col_name_e] = str(df.iloc[i].get(col_name_c,''))
                    if col_name_e in filter_list:
                        lesson_filter[col_name_e] = [str(model_lesson_data[col_name_e])]

                lessons, total = dao.Lesson.query_lessons(query_dict=lesson_filter, unscoped=False)
                if total == 0:
                    fail_lessons.append({**lesson_filter, 'reason': '没有课程'})
                    continue
                lesson_id = lessons[0]['lesson_id']
                term = lessons[0]['term']
                model_lesson_data['lesson_id'] = lesson_id
                model_lesson_data['unit'] = lessons[0]['lesson_unit']
                model_lesson_data['lesson_name'] = lessons[0]['lesson_name']
                model_lesson_data['lesson_teacher_name'] = lessons[0]['lesson_teacher_name']
                (_, num) = dao.ModelLesson.query_model_lessons(query_dict={
                    'lesson_id': [lesson_id],
                    'term': term
                    }, unscoped=False)
                if num != 0:
                    fail_lessons.append({**lesson_filter, 'reason': '好评课已经存在'})
                    continue
                model_lesson_data['term'] = term

                dao.Lesson.update_lesson(ctx=False, query_dict={'lesson_id': [lesson_id]},
                                            data={'lesson_model': '推荐为好评课'})
                dao.ModelLesson.insert_model_lesson(ctx=False, data=model_lesson_data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            raise e
        file_path = None
        if fail_lessons:
            frame_dict = {}
            other_model_data={}
            for file_lesson in fail_lessons:
                for key, value in column_dict.items():
                    if value in file_lesson:
                        excel_value = file_lesson.get(value)
                        if key not in frame_dict:
                            frame_dict[key] = [excel_value]
                        else:
                            frame_dict[key].append(excel_value)
                if file_lesson['reason'] == '没有课程':
                    name=file_lesson['lesson_name'][0]
                    for i in range(0, row_num):
                        import ipdb
                        ipdb.set_trace()
                        if df.iloc[i]['课程名称'] == name:
                            for key, value in column_dict.items():
                                other_model_data[value] = str(df.iloc[i].get(key, ''))
                            print(other_model_data)
                            dao.OtherModelLesson.insert_other_model_lesson(ctx=False, data={
                                'lesson_name':other_model_data['lesson_name'],
                                'lesson_attribute':other_model_data['lesson_attribute'],
                                'term': '-'.join([other_model_data['lesson_year'],
                                                      str(other_model_data['lesson_semester'])]).replace(' ', ''),
                                'lesson_teacher_name':other_model_data['lesson_teacher_name'],
                                'unit':other_model_data['lesson_teacher_unit'],
                                'group_name':other_model_data['group_name'],
                                'using':'true'
                            })
            frame = pandas.DataFrame(frame_dict)
            from app import basedir
            filename = '/static/' + "fail" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            fullname = basedir + filename
            frame.to_excel(fullname, sheet_name='123', index=False, header=True)
        return fail_lessons

    @classmethod
    def export_lesson_excel(cls, data: dict = None):
        if data is None:
            data = dict()
        if 'term' in data:
            model_lessons, num = dao.ModelLesson.query_model_lessons(query_dict={'term': [data['term']]})
        else:
            model_lessons, num = dao.ModelLesson.query_model_lessons()
        column_dict = {'课程名称': 'lesson_name', '课程性质': 'lesson_attribute', '学分': 'lesson_grade', '开课学年': 'lesson_year',
                       '开课学期': 'lesson_semester', '任课教师名称': 'lesson_teacher_name', '任课教师所在学院': 'lesson_teacher_unit',
                       '指定小组': 'group_name', '投票次数': 'votes', '提交次数': 'notices'}
        frame_dict = dict()
        for model_lesson in model_lessons:
            lesson = dao.Lesson.get_lesson(query_dict={
                'lesson_id': model_lesson['lesson_id'],
                'term': model_lesson['term']
            }, unscoped=True)
            if lesson is None:
                raise CustomError(404, 404, 'lesson not found')
            for key, value in column_dict.items():
                excel_value = lesson[value] if value in lesson else model_lesson.get(value, "")
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
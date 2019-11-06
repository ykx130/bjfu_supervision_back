import app.core.dao as dao
from app.utils.Error import CustomError
from app.utils.kafka import send_kafka_message
from app.core.services import NoticeService, FormService, ModelLessonService, LessonService

from app import redis_cli
import json


class FormController(object):

    @classmethod
    def push_new_form_message(cls, form_model):
        """
        发送问卷新增的消息
        :param form_model:
        :return:
        """
        tmpl = '课程{lesson_name}, 级别:{lesson_level}, 教师: {lesson_teacher} ，于{created_at} 被{created_by} 评价， 评价者{guider}, 督导小组{group}.'
        NoticeService.push_new_message(
            username=form_model.get('meta', {}).get('guider'),
            notice={
                'title': '问卷新增',
                'body': tmpl.format(
                    lesson_name=form_model.get('meta', {}).get('lesson', {}).get('lesson_name', ''),
                    created_at=form_model.get('meta', {}).get('created_at'),
                    created_by=form_model.get('meta', {}).get('created_by'),
                    guider=form_model.get('meta', {}).get('guider_name'),
                    group=form_model.get('meta', {}).get('guider_group'),
                    lesson_level=form_model.get('meta', {}).get('lesson', {}).get('lesson_level', ''),
                    lesson_teacher=form_model.get('meta', {}).get('lesson', {}).get(
                        'lesson_teacher_name', '')
                )
            }
        )

    @classmethod
    def push_put_back_form_message(cls, form_model):
        """
        发送问卷打回的消息
        :param form_model:
        :return:
        """
        tmpl = '问卷 课程{lesson_name}, 级别:{lesson_level}, 教师: {lesson_teacher} ，于{created_at} 被打回， 评价者{guider}, 督导小组{group}.'
        NoticeService.push_new_message(
            username=form_model.get('meta', {}).get('guider'),
            notice={
                'title': '问卷打回',
                'body': tmpl.format(
                    lesson_name=form_model.get('meta', {}).get('lesson', {}).get('lesson_name', ''),
                    created_at=form_model.get('meta', {}).get('created_at'),
                    created_by=form_model.get('meta', {}).get('created_by'),
                    guider=form_model.get('meta', {}).get('guider_name'),
                    group=form_model.get('meta', {}).get('guider_group'),
                    lesson_level=form_model.get('meta', {}).get('lesson', {}).get('lesson_level', ''),
                    lesson_teacher=form_model.get('meta', {}).get('lesson', {}).get(
                        'lesson_teacher_name', '')
                )
            }
        )

    @classmethod
    def insert_form(cls, data: dict = None):
        if data is None:
            data = dict()
        meta = data.get('meta', {})
        lesson_id = meta.get('lesson', {}).get('lesson_id', None)
        if lesson_id is None:
            raise CustomError(500, 200, '课程不能为空')
        if not FormService.check_lesson_meta(meta):
            raise CustomError(500, 200, '该督导在该时间段, 听过别的课!时间冲突!')
        dao.Form.insert_form(data)
        

        form_model = dao.Form.formatter_total(data)
        LessonService.refresh_notices(data.get("meta", {}).get("lesson", {}).get("lesson_id"))        #刷新听课次数
        ModelLessonService.refresh_vote_nums(data.get("meta", {}).get("lesson", {}).get("lesson_id"))        #刷新好评课程次数
        send_kafka_message(topic='form_service',
                           method='add_form',
                           term=meta.get('term', None),
                           bind_meta_name=form_model.get('bind_meta_name', None),
                           username=meta.get('guider', None),
                           form_id=form_model.get('_id', ''),
                           lesson_id=lesson_id)
        cls.push_new_form_message(form_model)
        return True

    @classmethod
    def formatter(cls, form: dict):
        return form

    @classmethod
    def query_forms(cls, query_dict: dict = None, unscoped: bool = False, simple=False):
        if query_dict is None:
            query_dict = dict()
        (forms, total) = dao.Form.query_forms(query_dict=query_dict, unscoped=unscoped, simple=simple)
        return [cls.formatter(form) for form in forms], total

    @classmethod
    def find_form(cls, query_dict, unscoped=False):
        form = dao.Form.get_form(query_dict=query_dict, unscoped=unscoped)
        if form is None:
            raise CustomError(404, 404, 'form not found')
        return cls.formatter(form)

    @classmethod
    def delete_form(cls, _id=None):
        form = dao.Form.get_form(query_dict={'_id': _id})
        if form is None:
            raise CustomError(404, 404, 'form not found')
        dao.Form.delete_form(where_dict={'_id': _id})
        return True

    @classmethod
    def update_form(cls, _id=None, data: dict = None):
        if data is None:
            data = dict()
        form = dao.Form.get_form(query_dict={'_id': _id})
        if form is None:
            raise CustomError(404, 404, 'form not found')
        dao.Form.update_form({'_id': _id}, data)
        if 'status' in data:
            form = dao.Form.get_form(query_dict={'_id': _id})
            if form is None:
                raise CustomError(404, 404, 'form not found')
            lesson_id = form.get('meta', {}).get('lesson', {}).get('lesson_id', None)
            if data.get('status') == '待提交':
                send_kafka_message(topic='form_service',
                                   method='repulse_form',
                                   term=form.get('meta', {}).get('term', None),
                                   bind_meta_name=form.get('bind_meta_name', None),
                                   username=form.get('meta', {}).get('guider', None),
                                   form_id=form.get('_id', ''),
                                   lesson_id=lesson_id)
                cls.push_put_back_form_message(form)
            if data.get('status') == '已提交':
                send_kafka_message(topic='form_service',
                                   method='add_form',
                                   term=form.get('meta', {}).get('term', None),
                                   bind_meta_name=form.get('bind_meta_name', None),
                                   username=form.get('meta', {}).get('guider', None),
                                   form_id=form.get('_id', ''),
                                   lesson_id=lesson_id)

        return True

    @classmethod
    def get_form_map(cls, meta_name):
        item_map = []
        word_cloud = []
        if redis_cli.exists('form_service:{}:map'.format(meta_name)):
            item_map = json.loads(redis_cli.get('form_service:{}:map'.format(meta_name)))
        if redis_cli.exists('form_service:{}:word_cloud'.format(meta_name)):
            word_cloud = json.loads(redis_cli.get('form_service:{}:word_cloud'.format(meta_name)))

        return {
            'item_map': item_map,
            'word_cloud': word_cloud
        }

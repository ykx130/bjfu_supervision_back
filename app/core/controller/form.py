'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-09-20 17:42:33
@LastEditTime: 2019-09-21 17:27:05
@LastEditors: Please set LastEditors
'''
import app.core.dao as dao
from app.utils.Error import CustomError
from app.utils.kafka import send_kafka_message
from app.core.services import NoticeService
import datetime

from app import redis_cli
import json
import pandas

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
        dao.Form.insert_form(data)
        form_model = dao.Form.formatter_total(data)
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
    def query_forms(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        (forms, total) = dao.Form.query_forms(query_dict=query_dict, unscoped=unscoped)
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
    @classmethod
    def export_forms_excel(cls,data:dict=None):
        if data is None:
            data = dict()
        forms, num = dao.Form.query_forms(
            query_dict={
                'meta.term': data['term'],
                'bind_meta_name': data['bind_meta_name']
            },
            foramtter=dao.Form.formatter_total
            )
        meta_form_dict = {'当前学期':'term' ,'督导姓名':'guider_name','填表时间':'created_at'}
                     # '评价状态':'status''关注原因':''
        lesson_form_dict={'任课教师': 'lesson_teacher_name',	'教师所在学院':'lesson_teacher_unit',
                      '上课班级':'lesson_class','上课地点':'lesson_room','听课时间':'lesson_date',
                      '听课节次':'lesson_times','课程名称':'lesson_name','章节目录':'content'}
        frame_dict = dict()
        value_form_dict=dict()
        for form in forms:
            for key, value in meta_form_dict.items():
                excel_value = form['meta'].get(meta_form_dict[key]) 
                if key not in frame_dict:
                    frame_dict[key] = [excel_value]
                else:
                    frame_dict[key].append(excel_value)
            frame_dict['评价状态'] = form['status']
            for key, value in lesson_form_dict.items():
                lesson_value = form['meta']['lesson'].get(lesson_form_dict[key]) 
                if key not in frame_dict:
                    frame_dict[key] = [lesson_value]
                else:
                    frame_dict[key].append(lesson_value)
            for meta_k in form:
                if meta_k=='values':
                    values_form_list=form['values']
                    l=len(values_form_list)
                    for i in range(l):
                        if values_form_list[i]['item_type']=='radio_option':
                            key=values_form_list[i]['title']
                            #val=values_form_list[i]['payload']['options'][values_form_list[i]['value']-1]['label']
                            p_list = values_form_list[i]['payload']['options']
                            if values_form_list[i]['value']=='':
                                val=''
                            else:
                                for k in range(len(p_list)):
                                    if p_list[k]['value']==values_form_list[i]['value']:
                                        val=p_list[k]['label']
                            if key not in value_form_dict:
                                value_form_dict[key] = [val]
                            else:
                                value_form_dict[key].append(val)
            frame_dict.update(value_form_dict)
            #from ipdb import set_trace
            #set_trace()
        try:
            frame = pandas.DataFrame(frame_dict)
            from app import basedir
            filename = '/static/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            fullname = basedir + filename
            frame.to_excel(fullname, sheet_name='123',
                           index=False, header=True)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return filename
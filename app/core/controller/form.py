import app.core.dao as dao
from app.utils.Error import CustomError
from app.utils.kafka import send_kafka_message
from app.core.services import NoticeService, FormService, ModelLessonService, LessonService
import pandas
import datetime

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

        # 填充关注原因
        for form in forms:
            lesson_info = form.get("meta", {}).get("lesson",{})
            lesson_info["lesson_attention_reason"] = ""
            if lesson_info.get("lesson_level") == "关注课程":
                notice_lesson = dao.NoticeLesson.get_notice_lesson({
                    "lesson_id": lesson_info.get("lesson_id")
                })
                if notice_lesson:
                    lesson_info["lesson_attention_reason"] = notice_lesson["lesson_attention_reason"]
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
    def form_excel_export(cls,data:dict=None):
        """[表格导出]
        
        Keyword Arguments:
            data {dict} -- [term,bind_meta_name,]] (default: {None})
        
        Returns:
            [type] -- [filename]
        """
        
        if data is None:
            data = dict()
        print(data)
        forms,num=dao.Form.query_forms(query_dict=data) # 过滤选择符合条件的form
        meta_form_dict = {'当前学期':'term','督导姓名':'guider_name','填表时间':'created_at','指定小组':'guider_group'}
        lesson_form_dict={'任课教师':'lesson_teacher_name','教师所在学院':'lesson_teacher_unit',
                      '上课班级':'lesson_class','上课地点':'lesson_room','听课时间':'lesson_date',
                      '听课节次':'lesson_times','课程名称':'lesson_name','章节目录':'content', '课程等级':'lesson_level',
                      '关注原因':'lesson_attention_reason' }
        excel_dict=dict() # form内容
        option_dict=dict() # 选项内容


        for form in forms:

            lesson_info = form.get("meta", {}).get("lesson",{})
            lesson_info["lesson_attention_reason"] = ""
            if lesson_info.get("lesson_level") == "关注课程":
                notice_lesson = dao.NoticeLesson.get_notice_lesson({
                    "lesson_id": lesson_info.get("lesson_id")
                })
            
                if notice_lesson:
                    lesson_info["lesson_attention_reason"] = notice_lesson["lesson_attention_reason"]
            
            # 处理是否好评课
            model_lesson = dao.ModelLesson.get_model_lesson({
                    "lesson_id": lesson_info.get("lesson_id")
                }) 
            
            if not excel_dict.get('是否为好评课入围'):
                excel_dict['是否为好评课入围'] = list()
            
            excel_dict['是否为好评课入围'].append( (model_lesson is not None) )

            for key,value in meta_form_dict.items(): # 从form匹配meta_form_dict中的value 并将meta_form_dict中的key作为字段名
                excel_value=form['meta'][meta_form_dict[key]] 
                if key not in excel_dict:
                    excel_dict[key]=[excel_value]
                else:
                    excel_dict[key].append(excel_value)
            if not excel_dict.get('评价状态'):
                excel_dict["评价状态"] = list()
            excel_dict["评价状态"].append(form["status"])
            
            for key,value in lesson_form_dict.items(): # 从form匹配lesson_form_dict中的value 并将lesson_form_dict中的key作为字段名
                excel_value=form['meta']['lesson'].get(lesson_form_dict[key], '')
                if key not in excel_dict:
                    excel_dict[key]=[excel_value]
                else:
                    excel_dict[key].append(excel_value)
            
            for key in form: # 遍历form找到values
                #import ipdb; ipdb.set_trace()
                if key=='values':
                    options=form['values']
                    option_len=len(options)
                    
                    for i in range(option_len): # form中的单选项,提取item_name作为字段名,根据value得到选择项的label
                        if options[i]['item_type']=='radio_option':
                            key=options[i]['item_name']
                            choose=options[i]['payload']['options']
                            val=''
                            for key_choose in range(len(choose)):
                                if choose[key_choose]['value']==options[i]['value']:
                                    val=choose[key_choose]['label']                               
                            if key not in  option_dict:
                                option_dict[key]=[val]
                            else:
                                option_dict[key].append(val)
                        
                        if options[i]['item_type']=='raw_text': # form中的文本项,提取item_name作为字段名,根据value得到填写的文本
                            key=options[i]['item_name']
                            if key not in  option_dict:
                                option_dict[key]=[options[i]['value']]
                            else:
                                option_dict[key].append(options[i]['value'])
                        
                        if options[i]['item_type']=='checkbox_option': # form中的多选项,遍历options,将options中的label作为字段名,如果value中存在字段名则该字段的值为1,否则为0
                            for l in range(len(options[i]['payload']['options'])):
                                key=options[i]['payload']['options'][l]['label']
                                if key in options[i]['value']:
                                    value=1
                                else:
                                    value=0
                                if key not in  option_dict:
                                    option_dict[key]=[value]
                                else:
                                    option_dict[key].append(value)
            excel_dict.update(option_dict)       
  
        try:
            frame = pandas.DataFrame(excel_dict)
            from app import basedir
            filename = '/static/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            fullname = basedir + filename
            frame.to_excel(fullname, sheet_name='123', index=False, header=True)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return filename                    



import json
from app import redis_cli
from app.core import dao
from app.core.services import TermService
from app.core.const import UNIT_LIST

class PageDataController():

    @classmethod
    def get_page_data(cls):
        data_dict = {
            "sys:form_num": {},
            "sys:current_term_form_num": {},
            "sys:guider_num": 0,
            "sys:notice_lesson_num": 0,
            "sys:submitted_form": 0,
            "sys:wait_submitted_form": 0,
            "sys:form_unsatisfy_num":0,
            "sys:form_just_num": 0,
            "sys:form_statisfy_num": 0,
            "sys:current_term_submitted_form": 0,
            "sys:current_term_wait_submitted_form": 0,
        }
        
        # 计算已提交的问卷
        submitted_form = redis_cli.get("sys:submitted_form")
        if submitted_form is None:
            submitted_form = 0
        else:
            submitted_form = json.loads(submitted_form)

        # 计算当前学期已提交的问卷数量
        current_term_submitted_form = redis_cli.get("sys:current_term_submitted_form")
        if current_term_submitted_form is None:
            current_term_submitted_form = 0
        else:
            current_term_submitted_form = json.loads(current_term_submitted_form)

        # 计算当前学期【待提交、草稿】的问卷总数
        current_term_wait_submitted_form =redis_cli.get("sys:current_term_wait_submitted_form")
        if current_term_wait_submitted_form is None:
            current_term_wait_submitted_form = 0
        else:
            current_term_wait_submitted_form = json.loads(current_term_wait_submitted_form)

        # 计算带提交
        wait_submitted_form = redis_cli.get("sys:wait_submitted_form")
        if wait_submitted_form is None:
            wait_submitted_form = 0
        else:
            wait_submitted_form = json.loads(wait_submitted_form)

        form_statisfy_num = redis_cli.get("sys:form_statisfy_num") 
        form_just_num = redis_cli.get("sys:form_just_num")
        form_unsatisfy_num = redis_cli.get("sys:form_unsatisfy_num")

        data_dict["sys:form_statisfy_num"] = json.loads(form_statisfy_num) if form_statisfy_num else 0
        data_dict["sys:form_just_num"] = json.loads(form_just_num) if form_just_num else 0
        data_dict["sys:form_unsatisfy_num"] = json.loads(form_unsatisfy_num) if form_unsatisfy_num else 0

        data_dict["sys:wait_submitted_form"] = wait_submitted_form
        data_dict["sys:submitted_form"] = submitted_form
        data_dict["sys:current_term_submitted_form"] = current_term_submitted_form
        data_dict["sys:current_term_wait_submitted_form"] = current_term_wait_submitted_form
        now_term = TermService.get_now_term()
        data_dict["sys:guider_num"] = dao.Supervisor.count(query_dict={'term': [now_term['name']]})
        data_dict["sys:notice_lesson_num"] = dao.NoticeLesson.count(query_dict={'term': [now_term['name']]})
        form_num = {}
        for unit in UNIT_LIST:
            num = redis_cli.get('sys:form_num:{unit}'.format(unit=unit))
            if not num:
                num = 0
            form_num[unit] = int(num)
        data_dict["sys:form_num"] = form_num

        current_term_form_num = {}
        for unit in UNIT_LIST:
            current_term_num = redis_cli.get('sys:current_term_form_num:{unit}'.format(unit=unit))
            if not current_term_num:
                current_term_num = 0
            current_term_form_num[unit] = int(current_term_num)
        data_dict['sys:current_term_form_num'] = current_term_form_num
        return data_dict

import json
from app import redis_cli
from app.core import dao


class PageDataController():

    @classmethod
    def get_page_data(cls):
        data_dict = {
            "sys:form_num": {},
            "sys:guider_num": 0,
            "sys:notice_lesson_num": 0,
            "sys:submitted_form": 0,
            "sys:wait_submitted_form": 0
        }

        submitted_form = redis_cli.get("sys:submitted_form")
        if submitted_form is None:
            submitted_form = 0
        else:
            submitted_form = json.loads(submitted_form)

        wait_submitted_form = redis_cli.get("sys:wait_submitted_form")
        if wait_submitted_form is None:
            wait_submitted_form = 0
        else:
            wait_submitted_form = json.loads(wait_submitted_form)

        data_dict["sys:submitted_form"] = wait_submitted_form
        data_dict["sys:submitted_form"] = submitted_form
        data_dict["sys:guider_num"] = dao.Supervisor.count(query_dict={})
        data_dict["sys:notice_lesson_num"] = dao.NoticeLesson.count(query_dict={})
        return data_dict

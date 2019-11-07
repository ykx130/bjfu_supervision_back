import json
import jieba
from collections import Counter
from app import redis_cli
from app.core import dao
from app.core.const import UNIT_LIST

class InterfaceService:

    @classmethod
    def update_page_data(cls):
        """
        更新首页数据
        :return:
        """

        _, has_submitted_num = dao.Form.query_forms(query_dict={
            "status": ["已完成"]
        })
        _, wait_submitted_form_num = dao.Form.query_forms(query_dict={
            "status": ["待提交", "草稿"]
        })
        print("has_submitted_num", has_submitted_num, "wait", wait_submitted_form_num)
        for unit in UNIT_LIST:
            _, submit_unit_num = dao.Form.query_forms(query_dict={
                "status": ["已完成"],
                "meta.lesson.lesson_teacher_unit": [unit]
            })
            redis_cli.set('sys:form_num:{unit}'.format(unit=unit), str(submit_unit_num))
        redis_cli.set("sys:submitted_form", json.dumps(has_submitted_num))
        redis_cli.set("sys:wait_submitted_form", json.dumps(wait_submitted_form_num))
        


if __name__ == "__main__":
    InterfaceService.update_page_data()
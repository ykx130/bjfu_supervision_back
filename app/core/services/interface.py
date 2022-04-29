import json
import jieba
from collections import Counter
from app import redis_cli
from app.core import dao
from app.core.const import UNIT_LIST
from app.utils.mongodb import mongo

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
        #  待提交包含了草稿和待提交
        _, wait_submitted_form_num = dao.Form.query_forms(query_dict={
            "status": ["待提交", "草稿"]
        })

        # 当前学期已提交的问卷数量
        from . import term
        term = term.TermService.get_now_term_no_cache()['name']
        _, current_term_has_submitted_num = dao.Form.query_forms(query_dict={
            "status": ["已完成"],
            "meta.term": [term]
        })
        # 当前学期待提交的问卷数目
        _, current_term_wait_submitted_num = dao.Form.query_forms(query_dict={
            "status": ["待提交","草稿"],
            "meta.term": [term]
        })

        print("history:  has_submitted_num", has_submitted_num, "wait", wait_submitted_form_num)
        print("current_term:  has_submitted_num ", current_term_has_submitted_num, "wait", current_term_wait_submitted_num)
        for unit in UNIT_LIST:
            _, submit_unit_num = dao.Form.query_forms(query_dict={
                "status": ["已完成"],
                "meta.lesson.lesson_teacher_unit": [unit]
            })
            redis_cli.set('sys:form_num:{unit}'.format(unit=unit), str(submit_unit_num))

        # 当前学期 各学院评教情况统计
        for unit in UNIT_LIST:
            _, current_term_submit_unit_num = dao.Form.query_forms(query_dict={
                "status": ["已完成"],
                "meta.lesson.lesson_teacher_unit": [unit],
                "meta.term": [term],
            })
            redis_cli.set('sys:current_term_form_num:{unit}'.format(unit=unit), str(current_term_submit_unit_num))




        redis_cli.set("sys:submitted_form", json.dumps(has_submitted_num))
        redis_cli.set("sys:wait_submitted_form", json.dumps(wait_submitted_form_num))
        redis_cli.set("sys:current_term_submitted_form", json.dumps(current_term_has_submitted_num))
        redis_cli.set("sys:current_term_wait_submitted_form", json.dumps(current_term_wait_submitted_num))
        
    
        # 评价情况数据刷新
        satisfy_num = mongo.db.form.count({
            "values": {
                "$elemMatch":{ "title": "总体评价", "value":{
                    "$in": ["1","2"]
                } } 
            }
        })

        just_num = mongo.db.form.count({
            "values": {
                "$elemMatch":{ "title": "总体评价", "value":{
                    "$in": ["3"]
                } } 
            }
        })

        unsatisfy_num = mongo.db.form.count({
            "values": {
                "$elemMatch":{ "title": "总体评价", "value":{
                    "$in": ["4","5"]
                } } 
            }
        })

        print("总体评价 满意 {} 一般 {} 不满意 {}".format(satisfy_num, just_num, unsatisfy_num))
        redis_cli.set("sys:form_statisfy_num", json.dumps(satisfy_num))
        redis_cli.set("sys:form_just_num", json.dumps(just_num))
        redis_cli.set("sys:form_unsatisfy_num", json.dumps(unsatisfy_num))


if __name__ == "__main__":
    InterfaceService.update_page_data()
'''
@Author: your name
@Date: 2019-11-06 17:19:25
@LastEditTime: 2019-11-23 08:52:46
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /bjfu_supervision_back_ykx/app/core/services/model_lesson.py
'''
import json
from collections import Counter
from app import redis_cli
from app.core import dao

class LessonService:

    @classmethod
    def refresh_notices(cls, lesson_id):
        forms_total, num_total = dao.Form.query_forms(
            query_dict={
                "meta.lesson.lesson_id": lesson_id,
                "model_lesson.is_model_lesson":True,
                "status": "已完成"
            },
        )
        print("num_total ", num_total)
        dao.Lesson.update_lesson(
            query_dict={
            'lesson_id': lesson_id
            }, 
            data={
                "notices": num_total
            }
        )
    
    @classmethod
    def refresh_lesson_record(cls, guider):
        """
        刷新督导的听课记录
        :param message:
        :return:
        """
        print("刷新 guider : {}".format(guider))
        from . import term
        term = term.TermService.get_now_term_no_cache()['name']
        _, total = dao.Form.query_forms(query_dict={
            "meta.guider": guider.get("username"),
            "meta.term": term
        })

        forms, has_submit = dao.Form.query_forms(query_dict={
            "meta.guider": guider.get("username"),
            "meta.term":term,
            "status": "已完成"
        })

        _, wait_submit = dao.Form.query_forms(query_dict={
            "meta.guider": guider.get("username"),
            "meta.term":term,
            "status": ["待提交", "草稿"]
        })

        finish_times = {
            "finish_total_times":0,
            "finish_1_times": 0,
            "finish_2_times": 0,
            "finish_3_times": 0,
            "finish_4_times": 0
        }
        

        for form in forms:
            times = len(form.get("meta", {}).get("lesson", {}).get("lesson_times", []))
            finish_times["finish_total_times"] = finish_times["finish_total_times"] + times
            if times == 1:
                finish_times["finish_1_times"] = finish_times["finish_1_times"] + 1
            elif times == 2:
                finish_times["finish_2_times"] = finish_times["finish_2_times"] + 1
            elif times == 3:
                finish_times["finish_3_times"] = finish_times["finish_3_times"] + 1
            elif times == 4:
                finish_times["finish_4_times"] = finish_times["finish_4_times"] + 1
        
        print("数量 {} {} {}, 节次: {}".format(total, has_submit, wait_submit, finish_times))
        
        lesson_record = dao.LessonRecord.get_lesson_record(query_dict={
                "username": guider.get("username"),
                "term": term
        })

        if lesson_record:
            ok=dao.LessonRecord.update_lesson_record(
                query_dict={
                    "username": guider.get("username"),
                    "term": term
                },
                data={
                    "to_be_submitted": wait_submit,
                    "has_submitted": has_submit,
                    "total_times": total,
                    **finish_times
                }
            )
        else:
            dao.LessonRecord.insert_lesson_record(data={
                "username": guider.get("username"),
                "name": guider.get("name"),
                "group_name": guider.get("group_name"),
                "to_be_submitted": wait_submit,
                "has_submitted": has_submit,
                "total_times": total,
                "using": 1,
                "term": term,
                **finish_times
            })



        

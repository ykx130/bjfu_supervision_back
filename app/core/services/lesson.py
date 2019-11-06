'''
@Author: your name
@Date: 2019-11-06 17:19:25
@LastEditTime: 2019-11-06 20:01:25
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
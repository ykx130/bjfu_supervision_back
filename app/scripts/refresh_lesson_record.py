'''
@Author: your name
@Date: 2019-11-21 10:07:59
@LastEditTime: 2019-11-21 12:26:23
@LastEditors: Please set LastEditors
@Description: In User Settings Editfrom
@FilePath: /bjfu_supervision_back/app/scripts/refresh_lesson_record.py
'''

from app.core import dao
from app import app

ctx = app.app_context()
ctx.push()

term = "2019-2020-1"

def get_all_guider():

    guiders, num = dao.Supervisor.query_supervisors(query_dict={
        "term": term
    })
    return guiders


def inser_lesson_record():
    guiders = get_all_guider() 
    for guider in guiders:
        _, total = dao.Form.query_forms(query_dict={
            "meta.guider": guider.get("username"),
            "meta.term": term
        })

        _, has_submit = dao.Form.query_forms(query_dict={
            "meta.guider": guider.get("username"),
            "meta.term":term,
            "status": "已完成"
        })

        _, wait_submit = dao.Form.query_forms(query_dict={
            "meta.guider": guider.get("username"),
            "meta.term":term,
            "status": "待提交"
        })
        
        print("数量 {} {} {}".format(total, has_submit, wait_submit))
        dao.LessonRecord.insert_lesson_record(data={
            "username": guider.get("username"),
            "name": guider.get("name"),
            "group_name": guider.get("group_name"),
            "to_be_submitted": wait_submit,
            "has_submitted": has_submit,
            "total_times": total,
            "using": 1,
            "term": term
        })

if __name__ == "__main__":
    inser_lesson_record()
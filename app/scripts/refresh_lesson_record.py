'''
@Author: your name
@Date: 2019-11-21 10:07:59
@LastEditTime: 2019-11-22 11:41:34
@LastEditors: Please set LastEditors
@Description: In User Settings Editfrom
@FilePath: /bjfu_supervision_back/app/scripts/refresh_lesson_record.py
'''

from app.core import dao
from app import app
from app.core.services import LessonService
ctx = app.app_context()
ctx.push()


term = "2022-2023-1"

def get_all_guider():

    guiders, num = dao.Supervisor.query_supervisors(query_dict={
        "term": term
    })
    return guiders


def inser_lesson_record():
    guiders = get_all_guider() 
    for guider in guiders:
        LessonService.refresh_lesson_record(guider)

if __name__ == "__main__":
    inser_lesson_record()
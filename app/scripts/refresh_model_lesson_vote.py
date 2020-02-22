'''
@Author: your name
@Date: 2019-11-06 19:46:03
@LastEditTime: 2019-11-26 22:29:53
@LastEditors: Please set LastEditors
@Description: In User Settings Ediz
@FilePath: /bjfu_supervision_back_ykx/app/scripts/refresh_model_lesson_vote.py
'''

from app.core.services import LessonService,ModelLessonService
from app.core import dao
from app import app

ctx = app.app_context()
ctx.push()


def run():
    model_lessons, num = dao.ModelLesson.query_model_lessons()
    for model_lesson in model_lessons:
        print("更新: ", model_lesson['lesson_name'])
        LessonService.refresh_notices(model_lesson['lesson_id'])
        ModelLessonService.refresh_vote_nums(model_lesson['lesson_id'])
    
if __name__ == "__main__":
    run()
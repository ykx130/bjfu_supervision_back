'''
@Author: your name
@Date: 2019-11-06 19:31:57
@LastEditTime: 2019-11-06 19:32:06
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /bjfu_supervision_back_ykx/app/streaming/lesson_server.py
'''
from app.streaming import sub_kafka
from app.core.services import InterfaceService
from app.core import dao
from multiprocessing import Process, Queue


@sub_kafka('lesson_service')
def lesson_service_server(method, args):
    if not method:
        return
    if method == 'add_notice_lesson' or method == 'delete_notice_lesson':
        InterfaceService.update_page_data()
        # 更新首页
        pass


@sub_kafka('form_service')
def lesson_form_service_server(method, args):
    if not method:
        return
    if method == 'add_form' or method == 'repulse_form':
        _, total, = dao.Form.query_forms(query_dict={
            'meta.lesson.lesson_id': args.get("lesson_id"),
            "status": "已完成"
        })
        dao.Lesson.update_lesson(query_dict={
            'lesson_id': args.get("lesson_id")
        }, data={
            "lesson_state": "已完成" if total else "未完成",
            "notices": total
        })


if __name__ == '__main__':

    processes = [
        Process(target=lesson_service_server),
        Process(target=lesson_form_service_server)
    ]
    [p.start() for p in processes]
    [p.join() for p in processes]

from app.streaming import sub_kafka
from app.core import dao
from multiprocessing import Process, Queue


@sub_kafka('form_service')
def lesson_record_by_form_server(method, args):
    """
    接收到问卷提交或者打回更新听课记录
    :param message:
    :return:
    """
    if not method:
        return

    if method == 'add_form' or method == 'repulse_form':
        # 更新听课记录
        # _, total = dao.Form.query_form(query_dict={
        #     "username": args.get("username"),
        #     "term": args.get("term"),
        #     ""
        # })
        # dao.LessonRecord.update_lesson_record(
        #     query_dict={
        #         "username": args.get("username"),
        #         "term": args.get("term")
        #     },
        #     data={
        #         ""
        #     }
        # )
        # lesson_record_service.change_user_lesson_record_num(message.get('args', {}).get('username', None),
        #                                                     message.get('args', {}).get('term', None))
        #
        pass


@sub_kafka('user_service')
def user_service_server(method, args):
    if not method:
        return
    if method == 'add_supervisor':
        supervisor = dao.Supervisor.get_supervisor(username=args.get("username"), term=args.get("term"))
        dao.LessonRecord.insert_lesson_record(data={
            "username": supervisor.get("username"),
            "name": supervisor.get("name"),
            "group_name": supervisor.get("group"),
            "to_be_submitted": 0,
            "has_submitted": 0,
            "total_times": 0,
            "using": 1,
            "term": args.get("term")
        })

    if method == "update_supervisor":
        supervisor = dao.Supervisor.get_supervisor(username=args.get("username"), term=args.get("term"))
        dao.LessonRecord.update_lesson_record(
            query_dict={
                "username": supervisor.get("username"),

            },
            data={
                "name": supervisor.get("name"),
                "group_name": supervisor.get("group"),
                "using": 1,
                "term": args.get("term")
            })


if __name__ == '__main__':
    processes = [
        Process(target=lesson_record_by_form_server),
        Process(target=user_service_server)
    ]
    [p.start() for p in processes]
    [p.join() for p in processes]

from app import redis_cli
import json
from app.core.models.user import User
from app.streaming import sub_kafka

REDIS_NOTICES_KEY = "bjfu_supervision:notices:{username}:user"


def get_notices_num(username):
    """
    获取未读消息数量
    :param user:
    :return:
    """
    if not redis_cli.exists(REDIS_NOTICES_KEY.format(username=username)):
        return 0
    else:
        return redis_cli.llen(REDIS_NOTICES_KEY.format(username=username))


def get_newest_notices(username):
    """
    获取最新
    :param user:
    :return:
    """
    if not redis_cli.exists(REDIS_NOTICES_KEY.format(username=username)):
        return {
            "title": "",
            "body": ""
        }
    else:
        notice = redis_cli.rpop(REDIS_NOTICES_KEY.format(username=username))
        return json.loads(notice)


def push_new_message(username, notice):
    """
    推送消息
    :return:
    """
    notice_str = json.dumps(notice)
    redis_cli.lpush(REDIS_NOTICES_KEY.format(username=username), notice_str)
    return True


def push_new_form_message(form):
    """
    推送问卷新增的消息
    :return:
    """
    meta = form.get("meta")
    if not meta:
        return

    tmpl = "课程{lesson_name}, 级别:{lesson_level}, 教师: {lesson_teacher} ，于{created_at} 被{created_by} 评价， 评价者{guider}, 督导小组{group}."
    push_new_message('admin', {
        "title": "问卷新增",
        "body": tmpl.format(lesson_name=meta.get("lesson", {}).get("lesson_name", ''),
                            created_at=meta.get("created_at"),
                            created_by=meta.get("created_by"),
                            guider=meta.get("guider_name"),
                            group=meta.get("guider_group"),
                            lesson_level=meta.get("lesson", {}).get("lesson_level", ''),
                            lesson_teacher=meta.get("lesson", {}).get("lesson_teacher_name", '')
                            )
    })


@sub_kafka('form_service')
def notice_service_receiver(message):
    method = message.get("method")
    if not method:
        return
    if method == 'add_form':
        push_new_form_message(message.get("args", {}).get("form", {}))

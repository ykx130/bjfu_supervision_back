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


@sub_kafka('notice_service')
def notice_service_receiver(message):
    push_new_message(message.get("args", {}).get("username"), message.get("args", {}).get("msg"))

from app import redis_cli
import json
from app.core.models.user import User


REDIS_NOTICES_KEY = "bjfu_supervision:notices:{username}:user"


def get_notices_num(user):
    """
    获取未读消息数量
    :param user:
    :return:
    """
    if not redis_cli.exists(REDIS_NOTICES_KEY.format(username=user.username)):
        return 0
    else:
        return redis_cli.llen(REDIS_NOTICES_KEY.format(username=user.username))


def get_newest_notices(user):
    """
    获取最新
    :param user:
    :return:
    """
    if not redis_cli.exists(REDIS_NOTICES_KEY.format(username=user.username)):
        return {
            "title": "",
            "body": ""
        }
    else:
        notice = redis_cli.rpop(REDIS_NOTICES_KEY.format(username=user.username))
        return json.loads(notice)


def push_new_message(user, notice):
    """
    推送消息
    :return:
    """
    notice_str = json.dumps(notice)
    redis_cli.lpush(REDIS_NOTICES_KEY.format(username=user.username), notice_str)
    return True

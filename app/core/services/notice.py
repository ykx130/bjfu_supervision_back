import json
from app import redis_cli


class NoticeService:
    REDIS_NOTICES_KEY = "bjfu_supervision:notices:{username}:user"

    @classmethod
    def get_notices_num(cls, username):
        """
        获取未读消息数量
        :param user:
        :return:
        """
        if not redis_cli.exists(cls.REDIS_NOTICES_KEY.format(username=username)):
            return 0
        else:
            return redis_cli.llen(cls.REDIS_NOTICES_KEY.format(username=username))

    @classmethod
    def get_newest_notices(cls, username):
        """
        获取最新
        :param user:
        :return:
        """
        if not redis_cli.exists(cls.REDIS_NOTICES_KEY.format(username=username)):
            return {
                "title": "",
                "body": ""
            }
        else:
            notice = redis_cli.rpop(cls.REDIS_NOTICES_KEY.format(username=username))
            return json.loads(notice)

    @classmethod
    def push_new_message(cls,username, notice):
        """
        推送消息
        :return:
        """
        notice_str = json.dumps(notice)
        redis_cli.lpush(cls.REDIS_NOTICES_KEY.format(username=username), notice_str)
        return True

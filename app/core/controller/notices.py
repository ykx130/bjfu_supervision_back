from app.core.services import NoticeService

class NoticeController:

    @classmethod
    def get_notices_num(cls, user):
        """
        获取未读消息数量
        :param user:
        :return:
        """
        return NoticeService.get_notices_num(user)

    @classmethod
    def get_newest_notices(cls, user):
        """
        获取最新
        :param user:
        :return:
        """
        return NoticeService.get_newest_notices(user)

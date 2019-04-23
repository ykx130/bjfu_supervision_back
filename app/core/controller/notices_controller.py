from app.core.services import notices_service
from flask_login import login_required


@login_required
def get_notices_num(user):
    """
    获取未读消息数量
    :param user:
    :return:
    """
    return notices_service.get_notices_num(user)


@login_required
def get_newest_notices(user):
    """
    获取最新
    :param user:
    :return:
    """
    return notices_service.get_newest_notices(user)

from flask_login import current_user, login_required
from flask import jsonify, request
from app.http.handler import notices_blueprint
from app.core.controller import NoticeController
from app.utils import CustomError, args_to_dict

@notices_blueprint.route('/notices')
@login_required
def get_notices_num():
    try:
        num = NoticeController.get_notices_num(user=current_user.username)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        "total": num,
        'msg': '',

    }), 200


@notices_blueprint.route('/notices/newest')
@login_required
def get_newest_notice():
    try:
        notice = NoticeController.get_newest_notices(current_user.username)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'notice': notice
    })

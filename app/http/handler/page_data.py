from flask_login import current_user
from flask import jsonify, request
from app.http.handler import page_data_blueprint
from app.core.controller import PageDataController
from app.utils import CustomError, args_to_dict


@page_data_blueprint.route("/page_data")
def get_notices_num():
    try:
        data = PageDataController.get_page_data()
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        "data": data,
        'msg': '',

    }), 200

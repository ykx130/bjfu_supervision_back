from app.core.controllers import page_data_controller
from flask import jsonify
from app.http.handler.page_data import page_data_blueprint


@page_data_blueprint.route('/page_data')
def get_page_data():
    (data, err) = page_data_controller.get_page_data()
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'data': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'data': data,
        'message': ''
    }), 200

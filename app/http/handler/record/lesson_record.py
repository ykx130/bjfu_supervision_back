from app.http.handler.record import lesson_records_blueprint
from flask import request, jsonify
from app.core.controllers import lesson_record_controller


@lesson_records_blueprint.route('/lesson_records')
def get_lesson_records():
    (lesson_records, total, err) = lesson_record_controller.find_lesson_records(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'lesson_records': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'message': '',
        'lesson_records': lesson_records
    }), 200


@lesson_records_blueprint.route('/lesson_records/<int:id>')
def get_lesson_record(id):
    (lesson_record, err) = lesson_record_controller.find_lesson_record(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'lesson_record': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_record': lesson_record
    }), 200

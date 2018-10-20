from app.http.handler.record import lesson_records_blueprint
from flask import request, jsonify
from app.core.controllers import lesson_record_controller


@lesson_records_blueprint.route('/lesson_records')
def get_lesson_records():
    (lesson_records, total, err) = lesson_record_controller.find_lesson_records(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'total': 0,
            'lesson_records': []
        }), 500 if type(err) is not str else 200
    else:
        return jsonify({
            'code': 200,
            'total': total,
            'lesson_records': lesson_records
        }), 200


@lesson_records_blueprint.route('/lessons_records/<int:id>')
def get_lesson_record(id):
    (lesson_record, err) = lesson_record_controller.find_lesson_record(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'lesson_record': None
        }), 500 if type(err) is not str else 200
    if lesson_record is None:
        return jsonify({
            'code': 404,
            'lesson_record': None
        }), 404
    return jsonify({
        'code': 200,
        'lesson_records': lesson_record
    }), 200

from app.http.handler.lesson_record import lesson_record_blueprint
from flask import request, jsonify
from app.core.controllers import lesson_record_controller


@lesson_record_blueprint.route('/lesson_records')
def find_term_lesson_records():
    (lesson_records, num, err) = lesson_record_controller.find_term_lesson_records(request.args)
    if err is not None:
        if err is not None:
            return jsonify({
                'code': err.code,
                'message': err.err_info,
                'lesson_records': None,
                'total': None
            }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_records': lesson_records,
        'total': num
    }), 200


@lesson_record_blueprint.route('/lesson_records/history')
def find_lesson_records_history():
    (lesson_records, num, err) = lesson_record_controller.find_lesson_records_history(request.args)
    if err is not None:
        if err is not None:
            return jsonify({
                'code': err.code,
                'message': err.err_info,
                'lesson_records': None,
                'total': None
            }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_records': lesson_records,
        'total': num
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/history')
def find_lesson_record_history(username):
    (lesson_records, num, err) = lesson_record_controller.find_lesson_record_history(username, request.args)
    if err is not None:
        if err is not None:
            return jsonify({
                'code': err.code,
                'message': err.err_info,
                'lesson_records': None,
                'total': None
            }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_records': lesson_records,
        'total': num
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>')
def find_lesson_record(username, term):
    (lesson_record, err) = lesson_record_controller.find_lesson_record(username, term)
    if err is not None:
        if err is not None:
            return jsonify({
                'code': err.code,
                'message': err.err_info,
                'lesson_record': None,
            }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_record': lesson_record,
    }), 200


@lesson_record_blueprint.route('/lesson_records', methods=['POST'])
def insert_lesson_record():
    (ifSuccess, err) = lesson_record_controller.insert_lesson_record(request.json)
    if err is not None:
        if err is not None:
            return jsonify({
                'code': err.code,
                'message': err.err_info,
                'lesson_record': None,
            }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_record': None,
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>', methods=['DELETE'])
def delete_lesson_record(username, term):
    (ifSuccess, err) = lesson_record_controller.delete_lesson_record(username, term)
    if err is not None:
        if err is not None:
            return jsonify({
                'code': err.code,
                'message': err.err_info,
                'lesson_record': None,
            }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_record': None,
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>', methods=['PUT'])
def update_lesson_record(username, term):
    (ifSuccess, err) = lesson_record_controller.update_lesson_record(username, term, request.json)
    if err is not None:
        if err is not None:
            return jsonify({
                'code': err.code,
                'message': err.err_info,
                'lesson_record': None,
            }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson_record': None,
    }), 200

from app.http.handler import lesson_record_blueprint
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError, args_to_dict


@lesson_record_blueprint.route('/lesson_records')
def find_term_lesson_records():
    term = request.args.get('term', None)
    try:
        (lesson_records, num) = controller.LessonRecordController.query_lesson_records_term(term=term,
                                                                                            query_dict=args_to_dict(
                                                                                                request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lesson_records': lesson_records,
        'total': num
    }), 200


@lesson_record_blueprint.route('/lesson_records/history')
def find_lesson_records_history():
    try:
        (lesson_records, num) = controller.LessonRecordController.query_lesson_records_history(
            query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lesson_records': lesson_records,
        'total': num
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/history')
def find_lesson_record_history(username):
    try:
        (lesson_records, num) = controller.LessonRecordController.query_lesson_record_history(username=username,
                                                                                              query_dict=args_to_dict(
                                                                                                  request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lesson_records': lesson_records,
        'total': num
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>')
def find_lesson_record(username, term):
    try:
        lesson_record = controller.LessonRecordController.get_lesson_record(username=username, term=term)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lesson_record': lesson_record,
    }), 200


@lesson_record_blueprint.route('/lesson_records', methods=['POST'])
def insert_lesson_record():
    try:
        controller.LessonRecordController.insert_lesson_record(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>', methods=['DELETE'])
def delete_lesson_record(username, term):
    try:
        controller.LessonRecordController.delete_lesson_record(username=username, term=term)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>', methods=['PUT'])
def update_lesson_record(username, term):
    try:
        controller.LessonRecordController.update_lesson_record(username=username, term=term, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200

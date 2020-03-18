from app.http.handler import lesson_record_blueprint
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError, args_to_dict, db
from flask import g
from flask_login import login_required
from app.http.handler.filter import Filter


@lesson_record_blueprint.route('/lesson_records')
@login_required
@Filter.filter_permission()
def find_term_lesson_records(**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    print(kwargs)
    try:
        (lesson_records, num) = controller.LessonRecordController.query_lesson_records_term(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
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
@login_required
@Filter.filter_permission()
def find_lesson_records_history(*args, **kwargs):
    try:
        (lesson_records, num) = controller.LessonRecordController.query_lesson_records_history(query_dict=kwargs)
    except CustomError as e:
        db.session.rollback()
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
@login_required
@Filter.filter_permission()
def find_lesson_record_history(username, **kwargs):
    try:
        query_dict = kwargs
        query_dict.update({'username':username})
        (lesson_records, num) = controller.LessonRecordController.query_lesson_record_history(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
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
@login_required
@Filter.filter_permission()
def find_lesson_record(username, term, **kwargs):
    query_dict = kwargs
    query_dict.update({'username':username, 'term':term})
    try:
        lesson_record = controller.LessonRecordController.get_lesson_record(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
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
@login_required
def insert_lesson_record(**kwargs):
    try:
        controller.LessonRecordController.insert_lesson_record(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>', methods=['DELETE'])
@login_required
def delete_lesson_record(username, term, **kwargs):
    try:
        controller.LessonRecordController.delete_lesson_record(username=username, term=term)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@lesson_record_blueprint.route('/lesson_records/<string:username>/term/<string:term>', methods=['PUT'])
@login_required
def update_lesson_record(username, term, **kwargs):
    try:
        controller.LessonRecordController.update_lesson_record(username=username, term=term, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@lesson_record_blueprint.route('/lesson_records/excel/export', methods=['POST'])
@login_required
def export_lesson_excel():
    try:
        filename = controller.LessonRecordController.export_lesson_record(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'filename': filename
    }), 200

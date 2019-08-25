from app.http.handler import model_lesson_blueprint
from flask import request, jsonify
import app.core.controller as controller
from flask_login import login_required
from app.http.handler.filter import Filter
from app.utils import CustomError, args_to_dict


@model_lesson_blueprint.route('/model_lessons')
@login_required
@Filter.filter_permission()
def find_model_lessons(*args, **kwargs):
    try:
        (model_lessons, total) = controller.ModelLessonController.query_model_lessons(query_dict=kwargs)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'model_lessons': model_lessons,
        'msg': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons', methods=['POST'])
@login_required
def insert_model_lesson():
    try:
        controller.ModelLessonController.insert_model_lesson(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons/batch', methods=['POST'])
@login_required
def insert_model_lessons():
    try:
        controller.ModelLessonController.insert_model_lessons(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons/<int:id>')
@login_required
@Filter.filter_permission()
def find_model_lesson(id, *args, **kwargs):
    try:
        query_dict = kwargs
        query_dict.update({'id':id})
        model_lesson = controller.ModelLessonController.get_model_lesson(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'model_lesson': model_lesson
    }), 200


@model_lesson_blueprint.route('/model_lessons/<int:id>', methods=['DELETE'])
@login_required
def delete_model_lesson(id):
    try:
        controller.ModelLessonController.delete_model_lesson(id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons', methods=['DELETE'])
@login_required
def delete_model_lessons():
    try:
        controller.ModelLessonController.delete_model_lessons(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons/<int:id>', methods=['PUT'])
@login_required
def update_model_lesson(id):
    try:
        controller.ModelLessonController.update_model_lesson(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons/<string:lesson_id>/vote', methods=['POST'])
@login_required
def model_lesson_vote(lesson_id):
    try:
        controller.ModelLessonController.model_lesson_vote(lesson_id=lesson_id, vote=request.json.get('vote', True))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons/excel/import', methods=['POST'])
@login_required
def import_lesson_excel():
    try:
        path = controller.ModelLessonController.import_lesson_excel(data=request)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    if path is None:
        return jsonify({
            'code': 200,
            'msg': '',
            'fail_excel_path': path
        }), 200
    else:
        return jsonify({
            'code': 500,
            'msg': '',
            'fail_excel_path': path
        }), 200


@model_lesson_blueprint.route('/model_lessons/excel/export', methods=['POST'])
@login_required
def export_lesson_excel():
    try:
        filename = controller.ModelLessonController.export_lesson_excel(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'filename': filename
    }), 200

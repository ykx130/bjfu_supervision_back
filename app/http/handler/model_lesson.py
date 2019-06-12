from app.http.handler import model_lesson_blueprint
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError, args_to_dict


@model_lesson_blueprint.route('/model_lessons')
def find_model_lessons():
    try:
        (model_lessons, total) = controller.ModelLessonController.query_model_lessons(
            query_dict=args_to_dict(request.args))
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
def find_model_lesson(id):
    try:
        model_lesson = controller.ModelLessonController.get_model_lesson(id=id)
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

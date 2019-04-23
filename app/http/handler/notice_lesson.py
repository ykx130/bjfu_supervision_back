from app.http.handler import notice_lesson_blueprint
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError, args_to_dict


@notice_lesson_blueprint.route('/notice_lessons')
def find_notice_lessons():
    try:
        (notice_lessons, total) = controller.NoticeLessonController.query_notice_lessons(
            query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'notice_lessons': notice_lessons,
        'message': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons', methods=['POST'])
def insert_notice_lesson():
    try:
        controller.NoticeLessonController.insert_notice_lesson(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/batch', methods=['POST'])
def insert_notice_lessons():
    try:
        controller.NoticeLessonController.insert_notice_lessons(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/<int:id>')
def find_notice_lesson(id):
    try:
        notice_lesson = controller.NoticeLessonController.get_notice_lesson(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'notice_lesson': notice_lesson
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/<int:id>', methods=['DELETE'])
def delete_notice_lesson(id):
    try:
        controller.NoticeLessonController.delete_notice_lesson(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons', methods=['DELETE'])
def delete_notice_lessons():
    try:
        controller.NoticeLessonController.delete_notice_lessons(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/<int:id>', methods=['PUT'])
def update_notice_lesson(id):
    try:
        controller.NoticeLessonController.update_notice_lesson(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/excel/import', methods=['POST'])
def import_lesson_excel():
    try:
        controller.NoticeLessonController.import_lesson_excel(data=request)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'notice_lesson': None
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/excel/export', methods=['POST'])
def export_lesson_excel():
    try:
        filename = controller.NoticeLessonController.export_lesson_excel(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'filename': filename
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/<int:id>/vote', methods=['POST'])
def notice_lesson_vote(id):
    try:
        controller.NoticeLessonController.notice_lesson_vote(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200

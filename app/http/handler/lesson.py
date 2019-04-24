from app.http.handler import lesson_blueprint
from flask import jsonify, request
from app.utils.misc import convert_datetime_to_string
import app.core.controller as controller
from app.utils.url_condition.url_condition_mongodb import dict_serializable
from app.utils import CustomError, args_to_dict


@lesson_blueprint.route('/lessons', methods=['POST'])
def new_lesson():
    try:
        controller.LessonController.update_database()
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@lesson_blueprint.route('/lessons')
def get_lessons():
    try:
        (lessons, num) = controller.LessonController.query_lessons(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lessons': lessons,
        'total': num,
    }), 200


@lesson_blueprint.route('/lessons/<string:lesson_id>')
def get_lesson(lesson_id):
    try:
        lesson = controller.LessonController.get_lesson(lesson_id=lesson_id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson': lesson
    }), 200


@lesson_blueprint.route('/lessons/<string:lesson_id>', methods=['PUT'])
def update_lesson(lesson_id):
    try:
        controller.LessonController.update_lesson(lesson_id=lesson_id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@lesson_blueprint.route('/terms')
def get_terms():
    try:
        (terms, total) = controller.TermController.query_terms(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'terms': terms,
        'total': total,
        'message': ''
    }), 200


@lesson_blueprint.route('/terms/current')
def get_term_now():
    try:
        term = controller.TermController.get_now_term()
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'term': term
    }), 200

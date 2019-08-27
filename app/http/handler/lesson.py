from app.http.handler import lesson_blueprint
from flask import jsonify, request
from app.utils.misc import convert_datetime_to_string
import app.core.controller as controller
from app.utils.url_condition.url_condition_mongodb import dict_serializable
from app.utils import CustomError, args_to_dict
from flask_login import login_required
from app.http.handler.filter import Filter


@lesson_blueprint.route('/lessons', methods=['POST'])
@login_required
def new_lesson():
    try:
        controller.LessonController.update_database(info=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@lesson_blueprint.route('/lessons')
@login_required
def get_lessons(*args, **kwargs):
    try:
        (lessons, num) = controller.LessonController.query_lessons(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lessons': lessons,
        'total': num,
    }), 200


@lesson_blueprint.route('/lessons_with_case')
@login_required
def get_lessons_with_case(*args, **kwargs):
    try:
        (lessons, num) = controller.LessonController.query_lessons_with_cases(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lessons': lessons,
        'total': num,
    }), 200


@lesson_blueprint.route('/lesson_cases')
@login_required
def query_lesson_cases(*args, **kwargs):
    try:
        (lessons, num) = controller.LessonCaseController.query_lesson_cases(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lesson_cases': lessons,
        'total': num,
    }), 200


@lesson_blueprint.route('/lessons/<string:lesson_id>')
@login_required
def get_lesson(lesson_id, *args, **kwargs):
    try:
        query_dict = args_to_dict(request.args)
        query_dict.update({'lesson_id': lesson_id})
        lesson = controller.LessonController.get_lesson(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'lesson': lesson
    }), 200


@lesson_blueprint.route('/lessons/<string:lesson_id>', methods=['PUT'])
@login_required
def update_lesson(lesson_id):
    try:
        controller.LessonController.update_lesson(lesson_id=lesson_id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@lesson_blueprint.route('/teacher_names', methods=['GET'])
@login_required
def get_teacher_names(*args, **kwargs):
    try:
        (teacher_names, total) = controller.LessonController.query_teacher_names(query_dict=args_to_dict(request.args),
                                                                                 unscoped=False)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'teacher_names': teacher_names,
        'total': total
    }), 200


@lesson_blueprint.route('/terms')
@login_required
def get_terms():
    query_dict = args_to_dict(request.args)
    query_dict['_sort'] = ['name']
    query_dict['_order'] = ['desc']
    try:
        (terms, total) = controller.TermController.query_terms(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'terms': terms,
        'total': total,
        'msg': ''
    }), 200


@lesson_blueprint.route('/terms/current')
@login_required
def get_term_now():
    try:
        term = controller.TermController.get_now_term()
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'term': term
    }), 200


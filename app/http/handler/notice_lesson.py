from app.http.handler import notice_lesson_blueprint
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError, args_to_dict, db
from flask_login import login_required
from app.http.handler.filter import Filter

@notice_lesson_blueprint.route('/notice_lessons')
@login_required
@Filter.filter_permission()
def find_notice_lessons(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (notice_lessons, total) = controller.NoticeLessonController.query_notice_lessons(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'notice_lessons': notice_lessons,
        'msg': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons', methods=['POST'])
@login_required
def insert_notice_lesson():
    try:
        controller.NoticeLessonController.insert_notice_lesson(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/batch', methods=['POST'])
@login_required
def insert_notice_lessons():
    try:
        controller.NoticeLessonController.insert_notice_lessons(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/<int:id>')
@login_required
@Filter.filter_permission()
def find_notice_lesson(id, *args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        query_dict = kwargs
        query_dict.update({'lesson_teacher_id':id})
        notice_lesson = controller.NoticeLessonController.get_notice_lesson(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'notice_lesson': notice_lesson
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/<int:id>', methods=['DELETE'])
@login_required
def delete_notice_lesson(id):
    try:
        controller.NoticeLessonController.delete_notice_lesson(lesson_teacher_id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons', methods=['DELETE'])
@login_required
def delete_notice_lessons():
    try:
        controller.NoticeLessonController.delete_notice_lessons(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/<int:id>', methods=['PUT'])
@login_required
def update_notice_lesson(id):
    try:
        controller.NoticeLessonController.update_notice_lesson(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/excel/import', methods=['POST'])
@login_required
def import_lesson_excel():
    try:
        path = controller.NoticeLessonController.import_lesson_excel(data=request)
    except CustomError as e:
        db.session.rollback()
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


@notice_lesson_blueprint.route('/notice_lessons/excel/export', methods=['POST'])
@login_required
def export_lesson_excel():
    try:
        filename = controller.NoticeLessonController.export_lesson_excel(data=request.json)
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


@notice_lesson_blueprint.route('/notice_lessons/<int:id>/vote', methods=['POST'])
@login_required
def notice_lesson_vote(id):
    try:
        controller.NoticeLessonController.notice_lesson_vote(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@notice_lesson_blueprint.route('/notice_lessons/teachers', methods=['GET'])
@login_required
@Filter.filter_permission()
def notice_lesson_teahcers(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (teachers, total) = controller.NoticeLessonController.query_notice_lessons_teachers(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'teachers': teachers,
        'total': total, 
        'msg': ''
    }), 200

import app.core.controller as controller
from flask import request, jsonify, url_for, json
from app.utils.misc import convert_datetime_to_string
from app.http.handler import user_blueprint
from app.utils import args_to_dict, CustomError, db
from flask_login import login_required
from app.http.handler.filter import Filter


@user_blueprint.route('/users')
@login_required
@Filter.fiilter_leader_unit_permission()
def query_users(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (users, total) = controller.UserController.query_users(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'users': users,
        'msg': ''
    }), 200


@user_blueprint.route('/users/<string:username>')
@login_required
def get_user(username, *args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    query_dict.update({'username': username})
    try:
        user = controller.UserController.get_user(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'user': user,
        'msg': '',
    }), 200


@user_blueprint.route('/users', methods=['POST'])
@login_required
def new_user():
    try:
        controller.UserController.insert_user(data=request.json)
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


@user_blueprint.route('/users/<string:username>/password', methods=['PUT'])
@login_required
def change_user_password(username):
    try:
        password = request.json.get('password', 'root')
        controller.UserController.change_user_password(username, password)
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


@user_blueprint.route('/users/excel/import', methods=['POST'])
@login_required
def import_users_excel():
    try:
        path = controller.UserController.import_users_excel(data=request)
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


@user_blueprint.route('/users/<string:username>', methods=['PUT'])
@login_required
def change_user(username):
    try:
        controller.UserController.update_user(username=username, data=request.json)
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


@user_blueprint.route('/users/<string:username>', methods=['DELETE'])
@login_required
def del_user(username):
    try:
        controller.UserController.delete_user(username=username)
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


@user_blueprint.route('/supervisors', methods=['GET'])
@login_required
@Filter.filter_permission()
def get_supervisors(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (supervisors, total) = controller.SupervisorController.query_supervisors(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'supervisors': supervisors,
        'msg': ''
    }), 200


@user_blueprint.route('/supervisors/expire', methods=['GET'])
@login_required
@Filter.filter_permission()
def find_supervisors_expire(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (supervisors, total) = controller.SupervisorController.query_supervisors_expire(
            query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'supervisors': supervisors,
        'msg': ''
    }), 200


@user_blueprint.route('/supervisors/batch_renewal', methods=['POST'])
@login_required
def batch_renewal():
    try:
        controller.SupervisorController.batch_renewal(data=request.json)
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


@user_blueprint.route('/supervisors', methods=['POST'])
@login_required
def insert_supervisor():
    try:
        controller.SupervisorController.insert_supervisor(data=request.json)
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


@user_blueprint.route('/supervisors/<int:id>', methods=['GET'])
@login_required
@Filter.filter_permission()
def get_supervisor(id, *args, **kwargs):
    query_dict = kwargs
    query_dict.update({'id': id})
    try:
        supervisor = controller.SupervisorController.get_supervisor(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'supervisor': supervisor
    }), 200


@user_blueprint.route('/supervisors/<int:id>', methods=['PUT'])
@login_required
def update_supervisor(id):
    try:
        controller.SupervisorController.update_supervisor(id=id, data=request.json)
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


@user_blueprint.route('/groups', methods=['GET'])
@login_required
@Filter.filter_permission()
def get_groups(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (groups, total) = controller.GroupController.query_groups(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'groups': groups,
        'total': total,
        'msg': ''
    }), 200

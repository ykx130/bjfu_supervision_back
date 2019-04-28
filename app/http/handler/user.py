import app.core.controller as controller
from flask import request, jsonify, url_for, json
from app.utils.misc import convert_datetime_to_string
from app.http.handler import user_blueprint
from app.utils import args_to_dict, CustomError


@user_blueprint.route('/users')
def query_users():
    try:
        (users, total) = controller.UserController.query_users(query_dict=args_to_dict(request.args))
    except CustomError as e:
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
def get_user(username):
    try:
        user = controller.UserController.get_user(username=username)
    except CustomError as e:
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
def new_user():
    try:
        controller.UserController.insert_user(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@user_blueprint.route('/users/<string:username>', methods=['PUT'])
def change_user(username):
    try:
        controller.UserController.update_user(username=username, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@user_blueprint.route('/users/<string:username>', methods=['DELETE'])
def del_user(username):
    try:
        controller.UserController.delete_user(username=username)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@user_blueprint.route('/supervisors', methods=['GET'])
def get_supervisors():
    try:
        (supervisors, total) = controller.SupervisorController.query_supervisors(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'users': supervisors,
        'msg': ''
    }), 200


@user_blueprint.route('/supervisors/expire', methods=['GET'])
def find_supervisors_expire():
    try:
        (supervisors, total) = controller.SupervisorController.query_supervisors_expire(
            query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'users': supervisors,
        'msg': ''
    }), 200


@user_blueprint.route('/supervisors/batch_renewal', methods=['POST'])
def batch_renewal():
    try:
        controller.SupervisorController.batch_renewal(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@user_blueprint.route('/supervisors', methods=['POST'])
def insert_supervisor():
    try:
        controller.SupervisorController.insert_supervisor(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@user_blueprint.route('/supervisors/<string:username>/term/<string:term>')
def get_supervisor(username, term):
    try:
        supervisor = controller.SupervisorController.get_supervisor(username=username, term=term)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'supervisor': supervisor
    }), 200


@user_blueprint.route('/supervisors/<string:username>/term/<string:term>', methods=['PUT'])
def update_supervisor(username, term):
    try:
        controller.SupervisorController.update_supervisor(username=username, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@user_blueprint.route('/groups', methods=['GET'])
def get_groups():
    try:
        (groups, total) = controller.GroupController.query_groups(query_dict=args_to_dict(request.args))
    except CustomError as e:
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

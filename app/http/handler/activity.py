from app.http.handler import activity_blueprint
from flask import request, jsonify
from flask_login import login_required
import app.core.controller  as controller
from flask_login import current_user
from app.utils import CustomError, args_to_dict
from app.http.handler.filter import Filter


@activity_blueprint.route('/activities')
@login_required
def find_activities(**kwargs):
    query_dict = {}
    query_dict.update(request.args)
    query_dict.update(kwargs)
    try:
        (activities, total) = controller.ActivityController.query_activities(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'activities': activities,
        'msg': ''
    }), 200


@activity_blueprint.route('/activities', methods=['POST'])
@login_required
def insert_activity(**kwargs):
    try:
        controller.ActivityController.insert_activity(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>')
@login_required
def find_activity(id, *args, **kwargs):
    try:
        query_dict = {}
        query_dict.update(kwargs)
        query_dict.update({'id': id})
        activity = controller.ActivityController.get_activity(query_dict={'id': id})
        (activity_users, num) = controller.ActivityUserController.query_activity_users(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity': activity,
        'activity_users': activity_users
    }), 200


@activity_blueprint.route('/activities/<int:id>', methods=['DELETE'])
@login_required
def delete_activity(id, **kwargs):
    try:
        controller.ActivityController.delete_activity(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>', methods=['PUT'])
@login_required
def update_activity(id, **kwargs):
    try:
        controller.ActivityController.update_activity(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users')
@login_required
def find_activity_users(id, **kwargs):
    try:
        query_dict = {}
        query_dict.update(request.args)
        query_dict.update(kwargs)
        activity = controller.ActivityController.get_activity(query_dict={'id': id})
        (activity_users, total) = controller.ActivityUserController.query_activity_users(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity': activity,
        'activity_users': activity_users
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users', methods=['POST'])
@login_required
def insert_activity_user(id, **kwargs):
    try:
        controller.ActivityUserController.insert_activity_user(activity_id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>')
@login_required
def find_activity_user(id, username, **kwargs):
    query_dict = {}
    query_dict.update(request.args)
    query_dict.update(kwargs)
    try:
        activity = controller.ActivityController.get_activity(query_dict=query_dict)
        activity_user = controller.ActivityUserController.get_activity_user(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity': activity,
        'activity_users': activity_user
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['DELETE'])
@login_required
def delete_activity_user(id, username, **kwargs):
    try:
        controller.ActivityUserController.delete_activity_user(activity_id=id, username=username)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['PUT'])
@login_required
def update_activity_user(id, username, **kwargs):
    try:
        controller.ActivityUserController.update_activity_user(activity_id=id, username=username, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@activity_blueprint.route('/current_user/activities')
@login_required
def get_current_user_activities(**kwargs):
    username = request.args['username'] if 'username' in request.args else current_user.username
    try:
        (activities, total) = controller.ActivityUserController.query_current_user_activities(username=username,
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
        'total': total,
        'activities': activities
    }), 200

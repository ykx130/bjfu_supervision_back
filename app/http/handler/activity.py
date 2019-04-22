from app.http.handler import activity_blueprint
from flask import request, jsonify
from flask_login import login_required
import app.core.controllers  as controller
from app.core.models.activity import ActivityUser
from flask_login import current_user
from app.utils import CustomError, args_to_dict


@activity_blueprint.route('/activities')
def find_activities():
    try:
        (activities, total) = controller.ActivityController.query_activities(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'activities': activities,
        'message': ''
    }), 200


@activity_blueprint.route('/activities', methods=['POST'])
def insert_activity():
    try:
        controller.ActivityController.insert_activity(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>')
def find_activity(id):
    try:
        activity = controller.ActivityController.get_activity(id=id)
        (activity_users, num) = controller.ActivityUserController.query_activity_users(activity_id=id,
                                                                                       query_dict=args_to_dict(
                                                                                           request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity,
        'activity_users': activity_users
    }), 200


@activity_blueprint.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    try:
        controller.ActivityController.delete_activity(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>', methods=['PUT'])
def update_activity(id):
    try:
        controller.ActivityController.update_activity(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users')
def find_activity_users(id):
    try:
        activity = controller.ActivityController.get_activity(id=id)
        (activity_users, total) = controller.ActivityUserController.query_activity_users(activity_id=id,
                                                                                         query_dict=args_to_dict(
                                                                                             request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity,
        'activity_users': activity_users
    }), 200


@login_required
@activity_blueprint.route('/activities/<int:id>/activity_users', methods=['POST'])
def insert_activity_user(id):
    try:
        controller.ActivityUserController.insert_activity_user(activity_id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>')
def find_activity_user(id, username):
    try:
        activity = controller.ActivityController.get_activity(id=id)
        activity_user = controller.ActivityUserController.get_activity_user(activity_id=id, username=username)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity,
        'activity_users': activity_user
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['DELETE'])
def delete_activity_user(id, username):
    try:
        controller.ActivityUserController.delete_activity_user(activity_id=id, username=username)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['PUT'])
def update_activity_user(id, username):
    try:
        controller.ActivityUserController.update_activity_user(activity_id=id, username=username, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@login_required
@activity_blueprint.route('/current_user/activities')
def get_current_user_activities():
    username = request.args['username'] if 'username' in request.args else current_user.username
    try:
        (activities, total) = controller.ActivityUserController.query_current_user_activities(username=username,
                                                                                              query_dict=args_to_dict(
                                                                                                  request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'total': total,
        'activities': activities
    }), 200

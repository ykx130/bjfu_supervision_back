from app.http.handler.activity import activity_blueprint
from flask import request, jsonify
from app.core.controllers.activity_controller import *


@activity_blueprint.route('/activities')
def get_activities():
    (activities, total, err) = find_activities(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'users': [],
            'total': 0
        }), 500
    return jsonify({
        'code': 200,
        'total': total,
        'activities': [activity_dict(activity) for activity in activities],
        'message': ''
    }), 200


@activity_blueprint.route('/activities', methods=['POST'])
def new_activity():
    (ifSuccess, err) = insert_activity(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': None
    })


@activity_blueprint.route('/activities/<int:id>')
def get_activity(id):
    (activity, err) = find_activity(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    (users, err) = find_activity_users(id, request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity_dict(activity),
        'activity_users': [activity_user_dict(id, user) for user in users]
    })


@activity_blueprint.route('/activities/<int:id>', methods=['DELETE'])
def del_activity(id):
    (ifSuccess, err) = delete_activity(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': None
    })


@activity_blueprint.route('/activities/<int:id>', methods=['PUT'])
def change_activity(id):
    (ifSuccess, err) = update_activity(id, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': None
    })


@activity_blueprint.route('/activities/<int:id>/users')
def get_activity_users(id):
    (activity, err) = find_activity(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    (users, total, err) = find_activity_users(id, request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': '',
            'activity': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity_dict(activity),
        'activity_users': [activity_user_dict(id, user) for user in users]
    })


@activity_blueprint.route('/activities/<int:id>/users', methods=['POST'])
def new_activity_user(id):
    (ifSuccess, err) = insert_activity_user(id, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': None,
        'activity_user': None
    })


@activity_blueprint.route('/activities/<int:id>/users/<string:username>')
def get_activity_user(id, username):
    (activity, err) = find_activity(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    (user, err) = find_activity_user(id, username)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity_dict(activity),
        'activity_user': activity_user_dict(id, user)
    })


@activity_blueprint.route('/activities/<int:id>/users/<string:username>', methods=['DELETE'])
def del_activity_user(id, username):
    (ifSuccess, err) = delete_activity_user(id, username)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': None,
        'activity_user': None
    })


@activity_blueprint.route('/activities/<int:id>/users/<string:username>', methods=['PUT'])
def change_activity_user(id, username):
    (ifSuccess, err) = update_activity_user(id, username, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': None,
        'activity_user': None
    })

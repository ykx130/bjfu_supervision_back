from app.http.handler.activity import activity_blueprint
from flask import request, jsonify
from flask_login import login_required
from app.core.controllers.activity_controller import *
from app.core.controllers.user_controller import find_user
from app.core.models.activity import ActivityUser
from flask_login import current_user


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
    if activity is None:
        return jsonify({
            'code': 404,
            'message': 'not found'
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity_dict(activity),
        'activity_users': [activity_user_dict(id, user) for user in activity.activity_users]
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


@activity_blueprint.route('/activities/<int:id>/activity_users')
def get_activity_users(id):
    (activity, err) = find_activity(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    if activity is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'activity': None
        }), 404
    (users, total, err) = find_activity_users(id, request.args)
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
        'activity_users': [activity_user_dict(id, user) for user in users]
    })


@login_required
@activity_blueprint.route('/activities/<int:id>/activity_users', methods=['POST'])
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


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>')
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


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['DELETE'])
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


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['PUT'])
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


@activity_blueprint.route('/current_user/activities')
def get_current_user_activities():
    (activities, total, err) = find_current_user_activities(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'total': 0,
            'activities': []
        }), 500 if type(err) is not str else 200
    username = request.args['username'] if 'username' in request.args else current_user.username
    (user, err) = find_user(username)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'total': 0,
            'activities': []
        }), 500 if type(err) is not str else 200
    if user is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'total': 0,
            'activities': []
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'total': total,
        'activities': [{'activity': activity_dict(activity),
                        'activity_user': {'state': ActivityUser.activity_user_state(activity.id, username).state,
                                          'fin_state': ActivityUser.activity_user_state(activity.id,
                                                                                        username).fin_state}} for
                       activity in activities] if request.args['state'] == 'hasAttended' else [
            {'activity': activity_dict(activity), 'activity_user': {'state': '未报名', 'fin_state': '未报名'}} for
            activity in activities]
    })

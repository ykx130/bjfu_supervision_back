from app.http.handler.activity import activity_blueprint
from flask import request, jsonify
from flask_login import login_required
from app.core.controllers import activity_controller
from app.core.controllers import user_controller
from app.core.models.activity import ActivityUser
from flask_login import current_user


@activity_blueprint.route('/activities')
def find_activities():
    (activities, total, err) = activity_controller.find_activities(request.args)
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
        'activities': activities,
        'message': ''
    }), 200


@activity_blueprint.route('/activities', methods=['POST'])
def insert_activity():
    (ifSuccess, err) = activity_controller.insert_activity(request.json)
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
def find_activity(id):
    (activity, activity_users, err) = activity_controller.find_activity(id)
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
        'activity': activity,
        'activity_users': activity_users
    })


@activity_blueprint.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    (ifSuccess, err) = activity_controller.delete_activity(id)
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
def update_activity(id):
    (ifSuccess, err) = activity_controller.update_activity(id, request.json)
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
def find_activity_users(id):
    (activity, err) = activity_controller.find_activity(id)
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
    (activity_users, total, err) = activity_controller.find_activity_users(id, request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity,
        'activity_users': activity_users
    })


@login_required
@activity_blueprint.route('/activities/<int:id>/activity_users', methods=['POST'])
def insert_activity_user(id):
    (ifSuccess, err) = activity_controller.insert_activity_user(id, request.json)
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
def find_activity_user(id, username):
    (activity, err) = activity_controller.find_activity(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 200 if type(err) is str else 500
    (activity_user, err) = activity_controller.find_activity_user(id, username)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'activity': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'activity': activity,
        'activity_user': activity_user
    })


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['DELETE'])
def delete_activity_user(id, username):
    (ifSuccess, err) = activity_controller.delete_activity_user(id, username)
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
def update_activity_user(id, username):
    (ifSuccess, err) = activity_controller.update_activity_user(id, username, request.json)
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
    username = request.args['username'] if 'username' in request.args else current_user.username
    (user, err) = user_controller.find_user(username)
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
    (activities, total, err) = activity_controller.find_current_user_activities(username, request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'total': 0,
            'activities': []
        }), 500 if type(err) is not str else 200
    return jsonify({
        'code': 200,
        'message': '',
        'total': total,
        'activities': activities
    })

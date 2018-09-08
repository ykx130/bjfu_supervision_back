from app.core.controllers import user_controller
from flask import request, jsonify, url_for, json
from app.utils.misc import convert_datetime_to_string
from app.http.handler.user import user_blueprint
from sqlalchemy.exc import IntegrityError


@user_blueprint.route('/users')
def get_users():
    (users, total, err) = user_controller.find_users(request.args)
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
        'users': [user_controller.user_to_dict(user) for user in users],
        'message': ''
    }), 200


@user_blueprint.route('/users/<string:username>')
def get_user(username):
    (user, err) = user_controller.find_user(username)
    if err is not None:
        return jsonify({
            'code': 500,
            'user': None,
            'message': str(err)
        }), 500
    if user is None:
        return jsonify({
            'code': 404,
            'message': 'there is no user'
        }), 404
    return jsonify({
        'code': 200,
        'user': user_controller.user_to_dict(user),
        'message': '',
    }), 200


@user_blueprint.route('/users', methods=['POST'])
def new_user():
    (user, err) = user_controller.find_user(request.json['username'])
    if err is not None:
        return jsonify({
            'code': 500,
            'user': None,
            'message': str(err)
        }), 500
    if user is not None:
        return jsonify({
            'code': 500,
            'message': 'the username has been used'
        })
    (_, err) = user_controller.insert_user(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'user': None,
            'message': str(err)
        }), 500
    return jsonify({
        'code': 200,
        'user': None,
        'message': ''
    }), 200


@user_blueprint.route('/users/<string:username>', methods=['PUT'])
def change_user(username):
    (user, err) = user_controller.find_user(username)
    if err is not None:
        return jsonify({
            'code': 500,
            'user': None,
            'message': str(err)
        }), 500
    if user is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'user': None
        }), 404
    (_, err) = user_controller.update_user(username, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'user': None,
            'message': str(err)
        }), 500
    return jsonify({
        'code': 200,
        'user': None,
        'message': ''
    }), 200


@user_blueprint.route('/users/<string:username>', methods=['DELETE'])
def del_user(username):
    (user, err) = user_controller.find_user(username)
    if err is not None:
        return jsonify({
            'code': 500,
            'user': None,
            'message': str(err)
        }), 500
    if user is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'user': None
        }), 404
    (_, err) = user_controller.delete_user(username)
    if err is not None:
        return jsonify({
            'code': 500,
            'user': None,
            'message': str(err)
        }), 500
    return jsonify({
        'code': 200,
        'user': None,
        'message': ''
    }), 200


@user_blueprint.route('/supervisiors', methods=['GET'])
def get_supervisiros():
    (supervisiors, total, err) = user_controller.find_supervisiors(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'users': [],
            'total': 0
        }), 200 if type(err) == str else 500
    return jsonify({
        'code': 200,
        'total': total,
        'users': [user_controller.user_to_dict(user) for user in supervisiors],
        'message': ''
    }), 200


@user_blueprint.route('/supervisiors_expire', methods=['GET'])
def find_supervisiors_expire():
    (supervisiors, total, err) = user_controller.find_supervisiors(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'users': [],
            'total': 0
        }), 200 if type(err) == str else 500
    return jsonify({
        'code': 200,
        'total': total,
        'users': [user_controller.user_to_dict(user) for user in supervisiors],
        'message': ''
    }), 200


@user_blueprint.route('/batch_renewal', methods=['POST'])
def batch_renewal():
    (ifSuccess, err) = user_controller.batch_renewal(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err)
        }), 200 if type(err) == str else 500
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@user_blueprint.route('/roles', methods=['GET'])
def get_roles():
    (roles, total, err) = user_controller.find_roles(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'roles': [],
            'total': 0
        }), 500
    return jsonify({
        'code': 200,
        'roles': [{
            'id': role.id,
            'name': role.name,
            'permissions': role.permissions
        } for role in roles],
        'total': total,
        'message': ''
    }), 200


@user_blueprint.route('/groups', methods=['GET'])
def get_groups():
    (groups, total, err) = user_controller.find_groups(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'total': 0,
            'groups': []
        }), 500
    return jsonify({
        'code': 200,
        'groups': [{
            'id': group.id,
            'name': group.name,
            'leader': user_controller.user_to_dict(group.leader)
        } for group in groups],
        'total': total,
        'message': ''
    }), 200

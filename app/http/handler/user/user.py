from app.core.controllers.user_controller import find_user, find_users, delete_user, update_user, insert_user, \
    find_roles, find_groups, has_user, user_to_dict
from flask import request, jsonify, url_for, json
from app.utils.misc import convert_datetime_to_string
from app.http.handler.user import user_blueprint
from sqlalchemy.exc import IntegrityError


@user_blueprint.route('/users')
def get_users():
    (users, total, err) = find_users(request.args)
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
        'users': [user_to_dict(user) for user in users],
        'message': ''
    }), 200


@user_blueprint.route('/users/<string:username>')
def get_user(username):
    (user, err) = find_user(username)
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
        'user': user_to_dict(user),
        'message': '',
    }), 200


@user_blueprint.route('/users', methods=['POST'])
def new_user():
    (user, err) = find_user(request.json['username'])
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
    (_, err) = insert_user(request.json)
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
    (user, err) = find_user(username)
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
    (_, err) = update_user(username, request.json)
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
    (user, err) = find_user(username)
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
    (_, err) = delete_user(username)
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


@user_blueprint.route('/roles', methods=['GET'])
def get_roles():
    (roles, total, err) = find_roles(request.args)
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
    (groups, total, err) = find_groups(request.args)
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
            'leader': user_to_dict(group.leader)
        } for group in groups],
        'total': total,
        'message': ''
    }), 200

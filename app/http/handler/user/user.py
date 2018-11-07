from app.core.controllers import user_controller
from flask import request, jsonify, url_for, json
from app.utils.misc import convert_datetime_to_string
from app.http.handler.user import user_blueprint


@user_blueprint.route('/users')
def get_users():
    (users, total, err) = user_controller.find_users(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'users': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'users': users,
        'message': ''
    }), 200


@user_blueprint.route('/users/<string:username>')
def get_user(username):
    (user, err) = user_controller.find_user(username)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'user': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'user': user,
        'message': '',
    }), 200


@user_blueprint.route('/users', methods=['POST'])
def new_user():
    (_, err) = user_controller.insert_user(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'user': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'user': None,
        'message': ''
    }), 200


@user_blueprint.route('/users/<string:username>', methods=['PUT'])
def change_user(username):
    (_, err) = user_controller.update_user(username, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'user': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'user': None,
        'message': ''
    }), 200


@user_blueprint.route('/users/<string:username>', methods=['DELETE'])
def del_user(username):
    (_, err) = user_controller.delete_user(username)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'user': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'user': None,
        'message': ''
    }), 200


@user_blueprint.route('/supervisors', methods=['GET'])
def get_supervisors():
    (supervisors, total, err) = user_controller.find_supervisors(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'users': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'users': supervisors,
        'message': ''
    }), 200


@user_blueprint.route('/supervisors/expire', methods=['GET'])
def find_supervisors_expire():
    (supervisors, total, err) = user_controller.find_supervisors_expire(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'users': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'users': supervisors,
        'message': ''
    }), 200


@user_blueprint.route('/supervisors/batch_renewal', methods=['POST'])
def batch_renewal():
    (ifSuccess, err) = user_controller.batch_renewal(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'user': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'user': None
    }), 200


@user_blueprint.route('/supervisors', methods=['POST'])
def insert_supervisor():
    (ifSuccess, err) = user_controller.insert_supervisor(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'user': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'user': None
    }), 200


@user_blueprint.route('/groups', methods=['GET'])
def get_groups():
    (groups, total, err) = user_controller.find_groups(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'groups': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'groups': groups,
        'total': total,
        'message': ''
    }), 200

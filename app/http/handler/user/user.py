from app.core.controllers.user_controller import find_user, find_users, delete_user, update_user, insert_user, find_roles, find_groups, has_user, user_to_json
from flask import request,jsonify,url_for,json
from app.utils.misc import convert_datetime_to_string
from app.http.handler.user import user_blueprint
from sqlalchemy.exc import IntegrityError

@user_blueprint.route('/users')
def get_users():
    try:
        users, total = find_users(request.args)
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        }),500
    return jsonify({
        'code':200,
        'total':total,
        'users':[user_to_json(user) for user in users]
    }),200


@user_blueprint.route('/users/<string:username>')
def get_user(username):
    try:
        user = find_user(username)
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        }),500
    if user is None:
        return jsonify({
            'code':404,
            'message':'there is no user'
        }),404
    return jsonify({
        'code': 200,
        'user': user_to_json(user)
    }),200

@user_blueprint.route('/users', methods=['POST'])
def new_user():
    if has_user(request.json['username']): #还需要加一层验证，用于排除一定的数据
        return jsonify({
            'code':500,
            'message':"the username has been used"
        }),200
    try:
        insert_user(request.json)
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'user': None
        }),500
    return jsonify({
        'code':200,
        'user':None
    }),200

@user_blueprint.route('/users/<string:username>', methods=['PUT'])
def change_user(username):
    if not has_user(username):
        return jsonify({
            'code':404,
            'message':"Not found"
        }),404
    if has_user(request.json['username']):
        return jsonify({
            'code':500,
            'message':'the username has been used'
        })
    try:
        update_user(username, request.json)
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'user': None
        }),500
    return jsonify({
        'code':200,
        'user':None
    }),200


@user_blueprint.route('/users/<string:username>', methods=['DELETE'])
def del_user(username):
    if not has_user(username):
        return jsonify({
            'code':404,
            'message':"Not Found"
        }),404
    try:
        delete_user(username)
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'user': None
        }),500
    return jsonify({
        'code':200,
        'user':None
    }),200


@user_blueprint.route('/roles',methods=['GET'])
def get_roles():
    try:
        roles, total = find_roles(request.args)
        roles = roles, total
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        }),500
    return jsonify({
        'code':200,
        'roles':[{
            'id':role.id,
            'name':role.name,
            'permissions':role.permissions
        } for role in roles],
        'total':total
    }),200


@user_blueprint.route('/groups',methods=['GET'])
def get_groups():
    try:
        groups, total = find_groups(request.args)
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        }),500
    return jsonify({
        'code':200,
        'groups':[{
            'id':group.id,
            'name':group.name,
            'leader':user_to_json(group.leader)
        } for group in groups],
        'total':total
    }),200



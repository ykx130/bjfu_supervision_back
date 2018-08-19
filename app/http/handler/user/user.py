from app.core.controllers.user_controller import find_user, find_users, delete_user, update_user, insert_user, find_roles, find_groups
from flask import request,jsonify,url_for,json
from app.utils.misc import convert_datetime_to_string
from app.http.handler.user import user_blueprint
from sqlalchemy.exc import IntegrityError

@user_blueprint.route('/users')
def get_users():
    try:
        pagination = find_users(request.args)
        users = pagination.items
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        })
    return jsonify({
        'code':200,
        'total':pagination.total,
        'users':[{
            'id':user.id,
            'username':user.username,
            'name':user.name,
            'start_time':convert_datetime_to_string(user.start_time),
            'end_time':convert_datetime_to_string(user.end_time),
            'sex':user.sex,
            'email':user.email,
            'phone':user.phone,
            'state':user.state,
            'unit':user.unit,
            'status':user.status,
            'work_state':user.work_state,
            'prorank':user.prorank,
            'skill':user.skill,
            'group':user.group,
            'role_names':[role.name for role in user.roles]
        } for user in users]
    })


@user_blueprint.route('/users/<string:username>')
def get_user(username):
    try:
        user = find_user(username)
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        })
    return jsonify({
        'code': 200,
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'start_time': convert_datetime_to_string(user.start_time),
            'end_time': convert_datetime_to_string(user.end_time),
            'sex': user.sex,
            'email': user.email,
            'phone': user.phone,
            'state': user.state,
            'unit': user.unit,
            'status': user.status,
            'work_state': user.work_state,
            'prorank': user.prorank,
            'skill': user.skill,
            'group': user.group,
            'role_names': [role.name for role in user.roles]
        }
    })

@user_blueprint.route('/users', methods=['POST'])
def new_user():
    try:
        insert_user(request.json)
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'user': None
        })
    return jsonify({
        'code':200,
        'user':None
    })

@user_blueprint.route('/users/<string:username>', methods=['PUT'])
def change_user(username):
    try:
        update_user(username, request.json)
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'user': None
        })
    return jsonify({
        'code':200,
        'user':None
    })


@user_blueprint.route('/users/<string:username>', methods=['DELETE'])
def del_user(username):
    try:
        delete_user(username)
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'user': None
        })
    return jsonify({
        'code':200,
        'user':None
    })


@user_blueprint.route('/roles',methods=['GET'])
def get_roles():
    try:
        pagination = find_roles(request.args)
        roles = pagination.items
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        })
    return jsonify({
        'code':200,
        'roles':[{
            'id':role.id,
            'name':role.name,
            'permissions':role.permissions
        } for role in roles],
        'total':pagination.total
    })


@user_blueprint.route('/groups',methods=['GET'])
def get_groups():
    try:
        pagination = find_groups(request.args)
        groups = pagination.items
    except Exception as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        })
    return jsonify({
        'code':200,
        'groups':[{
            'id':group.id,
            'name':group.name,
            'leader':{
                'id': group.leader.id,
                'username': group.leader.username,
                'name': group.leader.name,
                'start_time': convert_datetime_to_string(group.leader.start_time),
                'end_time': convert_datetime_to_string(group.leader.end_time),
                'sex': group.leader.sex,
                'email': group.leader.email,
                'phone': group.leader.phone,
                'state': group.leader.state,
                'unit': group.leader.unit,
                'status': group.leader.status,
                'work_state': group.leader.work_state,
                'prorank': group.leader.prorank,
                'skill': group.leader.skill,
                'group': group.leader.group,
                'role_names': [role.name for role in group.leader.roles]
            }
        } for group in groups],
        'total':pagination.total
    })



from app.http.handler.user import user_blueprint
from flask import request,jsonify,url_for,json
from pymongo.errors import ServerSelectionTimeoutError,PyMongoError
from app.core.controllers.common_controller import dict_serializable, UrlCondition, Paginate, object_to_str, sort_limit
from flask_pymongo import ObjectId
from app.core.controllers.user_controller import to_json_list, find_user,find_users, delete_user, insert_user, request_to_class,update_user,request_to_class_event,insert_event,find_event,delete_event,update_event


@user_blueprint.route('/users',methods=['POST'])
def new_user():
    from run import mongo
    user=request_to_class(request.json)
    try:
        insert_user(mongo,user)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'users':None
        }),500
    return jsonify({
        'code':200,
        'message':'',
        'users':None
    }),200

@user_blueprint.route('/users')
def get_users():
    url_condition=UrlCondition(request.args)
    from run import mongo
    try:
        users=find_users(mongo,url_condition.filter_dict)
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':str(e),
            'users':None
        }),500
    users=sort_limit(users,url_condition.sort_limit_dict)
    paginate=Paginate(users,url_condition.page_dict)
    users_list=[to_json_list(user) for user in paginate.data_page]
    prev=None
    if paginate.has_prev:
        prev=url_for('user_blueprint.get_users',_page=paginate.page-1)
    next=None
    if paginate.has_next:
        next=url_for('user_blueprint.get_users',_page=paginate.page+1)
    return jsonify({
        'code': '200',
        'message': '',
        'users': [object_to_str(users_list_node) for users_list_node in users_list],
        'prev': prev,
        'next': next,
        'has_prev': paginate.has_prev,
        'has_next': paginate.has_next,
        'total': paginate.total,
        'page_num': paginate.page_num,
        'page_now': paginate.page,
        'per_page': paginate.per_page
        }),200

@user_blueprint.route('/users/<string:_id>')
def get_user(_id):
    from run import mongo
    try:
        user_data=find_user(mongo, _id)
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message':str(e),
            'users':None
        }),500
    if user_data is None:
        return jsonify({
            'code': '404',
            'message':'Not found',
            'users':None
        }),404
    return jsonify({
        'code': '200',
        'message': '',
        'users': object_to_str(user_data)
    })

@user_blueprint.route('/users/<string:_id>',methods=['DELETE'])
def delete_user(_id):
    from run import mongo
    user=find_user(mongo,_id)
    if user is None:
        return jsonify({
            'code':404,
            'message':"Not found",
            "users":None
        }),404
    try:
        delete_user(mongo,{'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': str(e),
            'users':None
        }),500
    return jsonify({
        'code': '200',
        'message': '',
        'users':None
    }),200

@user_blueprint.route('/users/<string:_id>',methods=['PUT'])
def change_user(_id):
    from run import mongo
    user = find_user(mongo, _id)
    if user is None:
        return jsonify({
            'code': '404',
            'message': "No this user",
            "users": None
        }), 404
    try:
        update_user(mongo,{'_id':ObjectId(_id)},request.json)
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':str(e),
            'users':None
        }),500
    return jsonify({
        'code': '200',
        'message': '',
        'data': None
    }),200

@user_blueprint.route('/users/<string:_id>/events',methods=['POST'])
def new_event(_id):
    from run import mongo
    try:
        insert_event(request.json,mongo,_id)
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': e,
            'event':None
        }),500
    return jsonify({
        'code': '200',
        'message': '',
        'event':None
    }),200


@user_blueprint.route('/users/<string:_id>/events/<string:event_id>',methods=['GET'])
def get_event(_id,event_id):
    from run import mongo
    try:
        event=find_event(mongo,_id,event_id)
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message':e,
            'event': None
        }),500
    return jsonify({
        'code': '200',
        'message': '',
        'event': event
    }),200

@user_blueprint.route('/users/<string:_id>/events/<string:event_id>',methods=['DELETE'])
def delete_events(_id,event_id):
    from run import mongo
    try:
        delete_event(mongo,_id,event_id)
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': e,
            'event':None
        }),500
    return jsonify({
        'code': '200',
        'message': '',
        'event':None
    }),200

@user_blueprint.route('/users/<string:_id>/events/<string:event_id>',methods=['PUT'])
def change_event(_id,event_id):
    from run import mongo
    try:
        update_event(mongo,_id,event_id,request.json)
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':e,
            'event': None
        }),500
    return jsonify({
        'code': '200',
        'message': '',
        'event':None
    }),200


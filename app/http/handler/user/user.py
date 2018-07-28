from app.http.handler.user import user_blueprint
from flask import request,jsonify,url_for
from pymongo.errors import ServerSelectionTimeoutError,PyMongoError
from app.core.controllers.common_controller import dict_serializable, UrlCondition, Paginate, sort_limit
from flask_pymongo import ObjectId
from app.core.controllers.user_controller import to_json_list, find_user, delete_user, insert_user, request_to_class,request_to_class_event,update_event,find_event,delete_event

@user_blueprint.route('/users',methods=['POST'])
def new_user():
    from run import mongo
    user=request_to_class(request.json)
    try:
        insert_user(mongo,user)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code':500,
            'message':e
        })
    dict_json=dict_serializable(user.model)
    return jsonify({
        'code':200,
        'message':'',
        'data':[dict_json]
    })

@user_blueprint.route('/users')
def get_users():
    url_condition=UrlCondition(request.args)
    from run import mongo
    try:
        users=find_user(mongo,url_condition.filter_dict)
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':e
        })
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
        'data': [dict_serializable(users_list_node) for users_list_node in users_list],
        'prev': prev,
        'next': next,
        'has_prev': paginate.has_prev,
        'has_next': paginate.has_next,
        'total': paginate.total,
        'page_num': paginate.page_num,
        'page_now': paginate.page,
        'per_page': paginate.per_page
        })

@user_blueprint.route('/users/<string:id>')
def get_user(_id):
    from run import mongo
    try:
        user_datas=find_user(mongo,{'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message':e
        })
    return jsonify({
        'code': '200',
        'message': '',
        'data': [dict_serializable(user_data) for user_data in user_datas]
    })

@user_blueprint.route('/users/<string:id>',methods=['DELETE'])
def delete_user(_id):
    from run import mongo
    try:
        delete_user(mongo,{'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    return jsonify({
        'code': '200',
        'message': ''
    })

@user_blueprint.route('/users/<string:id>',methods=['PUT'])
def change_user(_id):
    from run import mongo
    try:
        delete_user(mongo, {'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':e
        })
        user = request_to_class(request.json)
    try:
        insert_user(mongo, user)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    dict_json = dict_serializable(user.model)
    return jsonify({
        'code': '200',
        'message': '',
        'data': [dict_json]
    })

@user_blueprint.route('/users/<string:id>/events',methods=['POST'])
def new_event(_id):
    from run import mongo
    events= request_to_class_event(request.json)
    try:
        user_datas=update_event(mongo,events,{'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    return jsonify({
        'code': '200',
        'message': '',
        'data': [dict_serializable(user_data) for user_data in user_datas]
    })

@user_blueprint.route('/users/<string:id>/events/<string:event_id>',methods=['POST'])
def get_event(_id,event_id):
    from run import mongo
    try:
        user_datas = find_user(mongo, {'_id': ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message':e
        })
    try:
        event=find_event(mongo,{'event_id': ObjectId(event_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message':e
        })
    user_datas['events']=[event]
    return jsonify({
        'code': '200',
        'message': '',
        'data': [dict_serializable(user_data) for user_data in user_datas]

    })

@user_blueprint.route('/users/<string:id>/events/<string:event_id>',methods=['DELETE'])
def delete_event(_id,event_id):
    from run import mongo
    try:
        delete_event(mongo,{'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    return jsonify({
        'code': '200',
        'message': ''
    })

@user_blueprint.route('/users/<string:id>/events/<string:event_id>',methods=['PUT'])
def change_event(_id,event_id):
    from run import mongo
    events = request_to_class_event(request.json)
    try:
        delete_event(mongo, {'event_id':ObjectId(event_id)})
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':e
        })
    try:
        user_datas = update_event(mongo, events, {'_id': ObjectId(_id)})
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    return jsonify({
        'code': '200',
        'message': '',
        'data': [dict_serializable(user_data) for user_data in user_datas]
    })


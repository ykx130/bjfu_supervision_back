from app.http.handler.item_type import item_type_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from app.core.controllers.item_type_controller import insert_item_type, delete_item_type, find_item_type, \
    update_item_type, request_to_class, dict_serializable, request_to_change


@item_type_blueprint.route('/item_types')
def get_item_types():
    from run import mongo
    try:
        item_types = find_item_type(mongo)
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(item_type) for item_type in item_types]
    })


@item_type_blueprint.route('/item_types', methods=['POST'])
def new_item_type():
    from run import mongo
    item_type = request_to_class(request.json)
    try:
        insert_item_type(mongo, item_type)
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(item_type.model)]
    })


@item_type_blueprint.route('/item_types/<string:_id>')
def get_item_type(_id):
    from run import mongo
    try:
        item_types = find_item_type(mongo, {'_id':ObjectId(_id)})
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(item_type) for item_type in item_types]
    })


@item_type_blueprint.route('/item_types/<string:_id>', methods= ['DELETE'])
def del_item_type(_id):
    from run import mongo
    try:
        delete_item_type(mongo, {'_id':ObjectId(_id)})
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[]
    })


@item_type_blueprint.route('/item_types/<string:_id>', methods=['PUT'])
def change_item_type(_id):
    from run import mongo
    change = request_to_change(request.json)
    try:
        update_item_type(mongo, {'_id':ObjectId(_id)}, change)
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[]
    })
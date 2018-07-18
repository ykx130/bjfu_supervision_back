from app.http.handler.item_type import item_type_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from flask import url_for
from app.core.controllers.item_type_controller import insert_item_type, delete_item_type, find_item_type, \
    update_item_type, request_to_class, request_to_change
from app.core.controllers.common_controller import dict_serializable, UrlCondition, sort_limit, Paginate


@item_type_blueprint.route('/item_types')
def get_item_types():
    url_condition = UrlCondition(request.args)
    from run import mongo
    try:
        item_types = find_item_type(mongo, url_condition.filter_dict)
    except:
        return jsonify({
            'code':'500',
            'message':''
        })
    item_types = sort_limit(item_types, url_condition.sort_limit_dict)
    paginate = Paginate(item_types, url_condition.page_dict)
    prev = None
    if paginate.has_prev:
        prev = url_for('item_type_blueprint.get_item_types', _page=paginate.page - 1)
    next = None
    if paginate.has_next:
        next = url_for('item_type_blueprint.get_item_types', _page=paginate.page + 1)
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(item_type) for item_type in item_types],
        'prev': prev,
        'next': next,
        'has_prev': paginate.has_prev,
        'has_next': paginate.has_next,
        'total': paginate.total,
        'page_num': paginate.page_num,
        'page_now': paginate.page,
        'per_page': paginate.per_page
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
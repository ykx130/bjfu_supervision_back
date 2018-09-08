from app.http.handler.item_type import item_type_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from app.core.controllers.item_type_controller import insert_item_type, delete_item_type, find_item_type, \
    update_item_type, request_to_class, request_to_change, find_item_types
from app.utils.url_condition.url_condition import UrlCondition, sort_limit, Paginate, object_to_str


@item_type_blueprint.route('/item_types')
def get_item_types():
    url_condition = UrlCondition(request.args)
    from run import mongo
    (item_types, err) = find_item_types(mongo, url_condition.filter_dict)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'item_types': [],
            'total': 0
        }), 500
    item_types = sort_limit(item_types, url_condition.sort_limit_dict)
    paginate = Paginate(item_types, url_condition.page_dict)
    return jsonify({
        'code': 200,
        'message': '',
        'item_types': [object_to_str(item_type) for item_type in item_types],
        'total': paginate.total,
    }), 200


@item_type_blueprint.route('/item_types', methods=['POST'])
def new_item_type():
    from run import mongo
    item_type = request_to_class(request.json)
    (_, err) = insert_item_type(mongo, item_type)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'item_type': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': None
    }), 200


@item_type_blueprint.route('/item_types/<string:_id>')
def get_item_type(_id):
    from run import mongo
    (item_type, err) = find_item_type(mongo, _id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'item_type': None
        }), 500
    if item_type is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'item_type': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': object_to_str(item_type) if item_type is not None else None
    }), 200


@item_type_blueprint.route('/item_types/<string:_id>', methods=['DELETE'])
def del_item_type(_id):
    from run import mongo
    (item_type, err) = find_item_type(mongo, _id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'item_type': None
        }), 500
    if item_type is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'item_type': None
        }), 404
    (_, err) = delete_item_type(mongo, {'_id': ObjectId(_id)})
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'item_type': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': None
    }), 200


@item_type_blueprint.route('/item_types/<string:_id>', methods=['PUT'])
def change_item_type(_id):
    from run import mongo
    (item_type, err) = find_item_type(mongo, _id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'item_type': None
        }), 500
    if item_type is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'item_type': None
        }), 404
    change = request_to_change(request.json)
    (_, err) = update_item_type(mongo, {'_id': ObjectId(_id)}, change)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'item_type': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': None
    }), 200

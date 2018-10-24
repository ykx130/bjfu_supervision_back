from app.http.handler.item_type import item_type_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from app.core.controllers import item_type_controller
from app.utils.url_condition.url_condition_mongodb import UrlCondition, sort_limit, Paginate, object_to_str


@item_type_blueprint.route('/item_types')
def get_item_types():
    (item_types, total, err) = item_type_controller.find_item_types(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'item_types': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'item_types': item_types,
        'total': total,
    }), 200


@item_type_blueprint.route('/item_types', methods=['POST'])
def new_item_type():
    (_, err) = item_type_controller.insert_item_type(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'item_type': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': None
    }), 200


@item_type_blueprint.route('/item_types/<string:_id>')
def get_item_type(_id):
    (item_type, err) = item_type_controller.find_item_type(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'item_type': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': item_type
    }), 200


@item_type_blueprint.route('/item_types/<string:_id>', methods=['DELETE'])
def del_item_type(_id):
    (item_type, err) = item_type_controller.find_item_type(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'item_type': None,
        }), err.status_code
    (_, err) = item_type_controller.delete_item_type({'_id': ObjectId(_id)})
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'item_type': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': None
    }), 200


@item_type_blueprint.route('/item_types/<string:_id>', methods=['PUT'])
def change_item_type(_id):
    (item_type, err) = item_type_controller.find_item_type(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'item_type': None,
        }), err.status_code
    (_, err) = item_type_controller.update_item_type({'_id': ObjectId(_id)}, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'item_type': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'item_type': None
    }), 200

from app.http.handler.block_type import block_type_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from app.core.controllers import block_type_controller


@block_type_blueprint.route('/block_types')
def find_block_types():
    (block_types, total, err) = block_type_controller.find_block_types(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'block_types': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'block_types': block_types,
        'total': total,
    }), 200


@block_type_blueprint.route('/block_types', methods=['POST'])
def insert_block_type():
    (ifSuccess, err) = block_type_controller.insert_block_type(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'block_type': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'block_type': None
    }), 200


@block_type_blueprint.route('/block_types/<string:_id>')
def find_block_type(_id):
    (block_type, err) = block_type_controller.find_block_type(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'block_type': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'block_type': block_type
    }), 200


@block_type_blueprint.route('/block_types/<string:_id>', methods=['DELETE'])
def del_block_type(_id):
    (block_type, err) = block_type_controller.find_block_type(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'block_type': None
        }), err.status_code
    (_, err) = block_type_controller.delete_block_type({'_id': ObjectId(_id)})
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'block_type': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'block_type': None
    }), 200


@block_type_blueprint.route('/block_types/<string:_id>', methods=['PUT'])
def change_block_type(_id):
    (block_type, err) = block_type_controller.find_block_type(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'block_type': None
        }), err.status_code
    (_, err) = block_type_controller.update_block_type({'_id': ObjectId(_id)}, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'block_type': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'block_type': None
    }), 200

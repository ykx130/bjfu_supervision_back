from flask import request, jsonify
import app.core.controller as controller
from app.http.handler import consult_blueprint
from app.utils import CustomError, args_to_dict


@consult_blueprint.route('/consults', methods=['POST'])
def new_consult():
    try:
        controller.ConsultController.insert_consult(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@consult_blueprint.route('/consults')
def get_consults():
    try:
        (consults, total) = controller.ConsultController.query_consults(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'total': total,
        'consults': consults
    }), 200


@consult_blueprint.route('/consults/<int:id>')
def get_consult(id):
    try:
        consult = controller.ConsultController.get_consult(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult': consult
    }), 200


@consult_blueprint.route('/consults/<int:id>', methods=['DELETE'])
def del_consult(id):
    try:
        controller.ConsultController.delete_consult(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@consult_blueprint.route('/consults/<int:id>', methods=['PUT'])
def change_consult(id):
    try:
        controller.ConsultController.update_consult(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': '200',
        'message': '',
    }), 200


@consult_blueprint.route('/consult_types', methods=['POST'])
def new_consult_type():
    try:
        controller.ConsultTypeController.insert_consult_type(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@consult_blueprint.route('/consult_types')
def get_consult_types():
    try:
        (consult_types, total) = controller.ConsultTypeController.query_consult_types(
            query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult_types': consult_types,
        'total': total
    }), 200


@consult_blueprint.route('/consult_types/<int:id>')
def get_consult_type(id):
    try:
        consult_type = controller.ConsultTypeController.get_consult_type(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult_type': consult_type
    }), 200


@consult_blueprint.route('/consult_types/<int:id>', methods=['DELETE'])
def del_consult_type(id):
    try:
        controller.ConsultTypeController.delete_consult_type(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@consult_blueprint.route('/consult_types/<int:id>', methods=['PUT'])
def change_consult_type(id):
    try:
        controller.ConsultTypeController.update_consult_type(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': '200',
        'message': '',
    }), 200

from flask import request, jsonify
import app.core.controller as controller
from app.http.handler import consult_blueprint
from flask_login import login_required
from app.http.handler.filter import Filter
from app.utils import CustomError, args_to_dict,db


@consult_blueprint.route('/consults', methods=['POST'])
@login_required
def new_consult():
    try:
        controller.ConsultController.insert_consult(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@consult_blueprint.route('/consults')
@login_required
def get_consults(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (consults, total) = controller.ConsultController.query_consults(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'total': total,
        'consults': consults
    }), 200


@consult_blueprint.route('/consults/<int:id>')
@login_required
def get_consult(id, *args, **kwargs):
    try:
        query_dict = kwargs
        query_dict.update({'id': id})
        consult = controller.ConsultController.get_consult(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'consult': consult
    }), 200


@consult_blueprint.route('/consults/<int:id>', methods=['DELETE'])
@login_required
def del_consult(id):
    try:
        controller.ConsultController.delete_consult(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@consult_blueprint.route('/consults/<int:id>', methods=['PUT'])
@login_required
def change_consult(id):
    try:
        controller.ConsultController.update_consult(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': '200',
        'msg': '',
    }), 200


@consult_blueprint.route('/consult_types', methods=['POST'])
@login_required
def new_consult_type():
    try:
        controller.ConsultTypeController.insert_consult_type(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@consult_blueprint.route('/consult_types')
@login_required
def get_consult_types(*args, **kwargs):
    try:
        query_dict = {}
        query_dict.update(args_to_dict(request.args))
        query_dict.update(kwargs)
        (consult_types, total) = controller.ConsultTypeController.query_consult_types(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'consult_types': consult_types,
        'total': total
    }), 200


@consult_blueprint.route('/consult_types/<int:id>')
@login_required
def get_consult_type(id, *args, **kwargs):
    query_dict = kwargs
    query_dict.update({'id': id})
    try:
        consult_type = controller.ConsultTypeController.get_consult_type(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'consult_type': consult_type
    }), 200


@consult_blueprint.route('/consult_types/<int:id>', methods=['DELETE'])
@login_required
def del_consult_type(id):
    try:
        controller.ConsultTypeController.delete_consult_type(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@consult_blueprint.route('/consult_types/<int:id>', methods=['PUT'])
@login_required
def change_consult_type(id):
    try:
        controller.ConsultTypeController.update_consult_type(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': '200',
        'msg': '',
    }), 200

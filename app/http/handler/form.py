import app.core.controller as controller
from flask_pymongo import ObjectId
from flask import jsonify, request
from flask_login import current_user, login_required
from app.http.handler import form_blueprint
from app.utils import CustomError, args_to_dict
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime


@form_blueprint.route('/forms', methods=['POST'])
@login_required
def new_form():
    request_json = request.json
    meta = request_json.get('meta', {})
    meta.update({'created_by': current_user.username,
                 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    request_json['meta'] = meta
    try:
        controller.FormController.insert_form(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@form_blueprint.route('/forms')
def query_forms():
    query_dict = args_to_dict(request.args)
    if not current_user.admin:
        if current_user.is_group is True:
            query_dict['meta.guider_group']: [current_user.username]
    try:
        (forms, total) = controller.FormController.query_forms(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'forms': forms,
        'total': total,
    }), 200


@form_blueprint.route('/forms/<string:_id>')
def get_form(_id):
    try:
        form = controller.FormController.find_form(_id=ObjectId(_id))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form': form
    }), 200


@form_blueprint.route('/forms/<string:_id>', methods=['DELETE'])
def delete_from(_id):
    try:
        controller.FormController.delete_form(_id=ObjectId(_id))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@form_blueprint.route('/forms/<string:_id>', methods=['PUT'])
def change_form(_id):
    try:
        controller.FormController.update_form(_id=ObjectId(_id), data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@form_blueprint.route('/my/forms')
@login_required
def get_my_forms():
    query_dict = args_to_dict(request.args)
    query_dict['meta.guider'] = [current_user.username]
    try:
        (forms, total) = controller.FormController.query_forms(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'forms': forms,
        'total': total,
    }), 200


@form_blueprint.route('/graph/form/<string:name>/map')
def get_form_map(name):
    return jsonify(controller.FormController.get_form_map(name))

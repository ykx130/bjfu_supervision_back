import app.core.controller as controller
from flask_pymongo import ObjectId
from flask import jsonify, request
from flask_login import current_user, login_required
from app.http.handler import form_blueprint
from app.utils import CustomError, args_to_dict, db
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
from app.http.handler.filter import Filter


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
        controller.FormController.insert_form(data=request_json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@form_blueprint.route('/forms')
@login_required
@Filter.filter_permission_mongo()
def query_forms(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (forms, total) = controller.FormController.query_forms(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'forms': forms,
        'total': total,
    }), 200


@form_blueprint.route('/forms/<string:_id>')
@login_required
@Filter.filter_permission_mongo()
def get_form(_id, *args, **kwargs):
    query_dict = kwargs
    query_dict.update({'_id':_id})
    try:
        form = controller.FormController.find_form(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'form': form
    }), 200


@form_blueprint.route('/forms/<string:_id>', methods=['DELETE'])
@login_required
def delete_from(_id):
    try:
        controller.FormController.delete_form(_id=ObjectId(_id))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@form_blueprint.route('/forms/<string:_id>', methods=['PUT'])
@login_required
def change_form(_id):
    try:
        controller.FormController.update_form(_id=ObjectId(_id), data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@form_blueprint.route('/my/forms')
@login_required
def get_my_forms():
    query_dict = args_to_dict(request.args)
    query_dict['meta.guider'] = [current_user.username]
    try:
        (forms, total) = controller.FormController.query_forms(query_dict=query_dict, simple=True)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'forms': forms,
        'total': total,
    }), 200


@form_blueprint.route('/graph/form/<string:name>/map')
@login_required
def get_form_map(name):
    return jsonify(controller.FormController.get_form_map(name))


@form_blueprint.route('/form/excel/export', methods=['POST'])
@login_required
def form_excel_export():
    try:
        filename = controller.FormController.form_excel_export(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'filename': filename
    }), 200

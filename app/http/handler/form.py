import app.core.controllers as core
from flask_pymongo import ObjectId
from flask import jsonify, request
from flask_login import current_user, login_required
from app.http.handler import form_blueprint
from app.utils.url_condition.url_condition_mysql import *
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime


@login_required
@form_blueprint.route('/forms', methods=['POST'])
def new_form():
    request_json = request.json
    meta = request_json.get('meta', {})
    meta.update({"created_by": current_user.username,
                 "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    request_json['meta'] = meta
    (_, err) = core.FormController.insert_form(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }), 200


@form_blueprint.route('/forms')
def get_forms():
    args = request.args
    if not current_user.admin:
        if current_user.is_group == True: args = ImmutableMultiDict(
            {**request.args, 'meta.guider_group': [current_user.username]})

    (forms, total, err) = core.FormController.query_forms(args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'forms': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'forms': forms,
        'total': total,
    }), 200


@form_blueprint.route('/forms/<string:_id>')
def get_form(_id):
    (form, err) = core.FormController.find_form(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form': form
    }), 200


@form_blueprint.route('/forms/<string:_id>', methods=['DELETE'])
def delete_from(_id):
    (form, err) = core.FormController.find_form(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code
    (_, err) = core.FormController.delete_form({'_id': ObjectId(_id)})
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }), 200


@form_blueprint.route('/forms/<string:_id>', methods=['PUT'])
def change_form(_id):
    (form, err) = core.FormController.find_form(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code

    (_, err) = core.FormController.update_form({'_id': ObjectId(_id)}, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }), 200


@login_required
@form_blueprint.route('/my/forms')
def get_my_forms():
    (forms, total, err) = core.FormController.query_forms(
        ImmutableMultiDict({**request.args, 'meta.guider': [current_user.username]}))
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'forms': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'forms': forms,
        'total': total,
    }), 200


@form_blueprint.route('/graph/form/<string:name>/map')
def get_form_map(name):
    return jsonify(core.FormController.get_form_map(name))

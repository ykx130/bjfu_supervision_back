import json
from app.http.handler.form import form_blueprint
from flask import jsonify, request
from werkzeug.datastructures import ImmutableMultiDict
from flask_login import current_user, login_required
from app.core.controllers import form_controller
from flask_pymongo import ObjectId


@form_blueprint.route('/forms', methods=['POST'])
def new_form():
    (_, err) = form_controller.insert_form(request.json)
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
    if '管理员' not in current_user.role_names:
        if current_user.is_group == True:
            args = {**request.args, 'meta.guider_group': [current_user.username]}

    (forms, total, err) = form_controller.find_forms(args)
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
    (form, err) = form_controller.find_form(_id)
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
    (form, err) = form_controller.find_form(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code
    (_, err) = form_controller.delete_form({'_id': ObjectId(_id)})
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
    (form, err) = form_controller.find_form(_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form': None,
        }), err.status_code

    (_, err) = form_controller.update_form({'_id': ObjectId(_id)}, request.json)
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
    (forms, total, err) = form_controller.find_forms(
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
    return jsonify(form_controller.get_form_map(name))

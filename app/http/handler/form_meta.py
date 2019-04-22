from flask import jsonify, request
from app.http.handler import form_meta_blueprint
from werkzeug.datastructures import ImmutableMultiDict
import app.core.controllers as controller
from flask_login import login_required, current_user
from datetime import datetime
from app.utils import CustomError, args_to_dict


@login_required
@form_meta_blueprint.route('/form_metas', methods=['POST'])
def insert_form_meta():
    request_json = request.json
    meta = request_json.get('meta', {})
    meta.update({'created_by': current_user.username,
                 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    request_json['meta'] = meta
    try:
        controller.FormMetaController.insert_form_meta(data=request_json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
    }), 200


@form_meta_blueprint.route('/form_metas')
def find_form_metas():
    try:
        (form_metas, total) = controller.FormMetaController.query_form_metas(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_metas': form_metas,
        'total': total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>')
def find_form_meta_name(name):
    try:
        form_meta = controller.FormMetaController.get_form_meta(name=name)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': form_meta
    }), 200


@form_meta_blueprint.route('/form_metas/history')
def find_history_form_metas():
    try:
        (form_metas, num) = controller.FormMetaController.query_form_meta()
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'total': num,
        'form_metas': form_metas
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/history')
def find_history_form_meta_by_name(name):
    try:
        (form_metas, total) = controller.FormMetaController.get_history_form_meta(name=name,
                                                                                  query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_metas': form_metas,
        'total': total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/version/<string:version>')
def get_form_meta(name, version):
    (form_meta, err) = controller.FormMetaController.get_form_meta(name, version)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': form_meta
    }), 200


@form_meta_blueprint.route('/form_metas/<name>', methods=['DELETE'])
def delete_form_meta(name):
    (form_meta, err) = controller.FormMetaController.get_form_meta(name)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    (_, err) = controller.FormMetaController.delete_form_meta({'name': name})
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>', methods=['PUT'])
def change_form_meta(name):
    (form_meta, err) = controller.FormMetaController.get_form_meta(name)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    (ifSuccessful, err) = controller.FormMetaController.update_form_meta(name, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }), 200

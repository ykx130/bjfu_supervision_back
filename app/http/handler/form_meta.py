from flask import jsonify, request
from app.http.handler import form_meta_blueprint
from werkzeug.datastructures import ImmutableMultiDict
import app.core.controller as controller
from flask_login import login_required, current_user
from datetime import datetime
from app.utils import CustomError, args_to_dict, db
from app.http.handler.filter import Filter


@form_meta_blueprint.route('/form_metas', methods=['POST'])
@login_required
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
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@form_meta_blueprint.route('/form_metas')
@login_required
def find_form_metas(*args, **kwargs):
    try:
        (form_metas, total) = controller.FormMetaController.query_form_metas(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'form_metas': form_metas,
        'total': total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>')
@login_required
def find_form_meta_name(name, *args, **kwargs):
    try:
        query_dict = args_to_dict(request.args)
        query_dict.update({'name': name})
        form_meta = controller.FormMetaController.get_form_meta(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'form_meta': form_meta
    }), 200


@form_meta_blueprint.route('/form_metas/history')
@login_required
def find_history_form_metas(*args, **kwargs):
    try:
        (form_metas, num) = controller.FormMetaController.query_form_metas(args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'total': num,
        'form_metas': form_metas
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/history')
@login_required
def find_history_form_meta_by_name(name, *args, **kwargs):
    try:
        query_dict = args_to_dict(request.args)
        query_dict.update({'name': name})
        (form_metas, total) = controller.FormMetaController.get_history_form_meta(query_dict=query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'form_metas': form_metas,
        'total': total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/version/<string:version>')
@login_required
def get_form_meta(name, version, *args, **kwargs):
    try:
        query_dict = args_to_dict(request.args)
        query_dict.update({'name': name, 'version':version})
        form_meta = controller.FormMetaController.get_form_meta(query_dict)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'form_meta': form_meta
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/version/<string:version>', methods=['DELETE'])
@login_required
def delete_form_meta(name, version):
    try:
        controller.FormMetaController.delete_form_meta(name, version)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'form_meta': None
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>', methods=['PUT'])
@login_required
def change_form_meta(name):
    try:
        controller.FormMetaController.update_form_meta(name=name, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'form_meta': None
    }), 200


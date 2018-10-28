from flask import jsonify, request
from app.http.handler.form_meta import form_meta_blueprint
from app.core.controllers import form_meta_controller
from werkzeug.datastructures import ImmutableMultiDict


@form_meta_blueprint.route('/form_metas', methods=['POST'])
def insert_form_meta():
    name = request.json['name'] if 'name' in request.json else None
    (old_form_meta, err) = form_meta_controller.find_form_meta(name)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    (ifSuccess, err) = form_meta_controller.insert_form_meta(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None,
    }), 200


@form_meta_blueprint.route('/form_metas')
def find_form_metas():
    (form_metas, total, err) = form_meta_controller.find_form_metas(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_metas': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_metas': form_metas,
        'total': total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>')
def find_form_meta_name(name):
    (form_meta, err) = form_meta_controller.find_form_metas()
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


@form_meta_blueprint.route('/form_metas/<string:name>/history')
def find_history_form_meta_by_name(name):
    (form_metas, total, err) = form_meta_controller.find_history_form_meta(ImmutableMultiDict(
        {"name": name}
    ))
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_metas': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'form_metas': form_metas,
        'total': total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/version/<string:version>')
def get_form_meta(name, version):
    (form_meta, err) = form_meta_controller.find_form_meta(name, version)
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
    (form_meta, err) = form_meta_controller.find_form_meta(name)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    (_, err) = form_meta_controller.delete_form_meta({'name': name})
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
    (form_meta, err) = form_meta_controller.find_form_meta(name)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'form_meta': None,
        }), err.status_code
    (ifSuccessful, err) = form_meta_controller.update_form_meta(name, request.json)
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

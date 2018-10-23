from flask import jsonify, request
from app.http.handler.form_meta import form_meta_blueprint
from app.core.controllers import form_meta_controller


@form_meta_blueprint.route('/form_metas', methods=['POST'])
def insert_form_meta():
    name = request.json['name'] if 'name' in request.json else None
    (old_form_meta, err) = form_meta_controller.find_form_meta(name)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err)
        })
    if old_form_meta is not None:
        return jsonify({
            'code': 500,
            'message': 'the name has been used'
        }), 200
    (ifSuccess, err) = form_meta_controller.insert_form_meta(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err)
        }), 500
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/form_metas')
def find_form_metas():
    (form_metas, total, err) = form_meta_controller.find_form_metas(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_metas': []
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form_metas': form_metas,
        'total': total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>')
def find_form_meta_name(name):
    if name is None:
        return jsonify({
            'code': 500,
            'message': 'name can not be null',
            'form_meta': None
        })
    (form_meta, err) = form_meta_controller.find_form_meta(name)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    if form_meta is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'form_meta': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': form_meta
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/<string:version>')
def get_form_meta(name, version):
    if name is None:
        return jsonify({
            'code': 500,
            'message': 'name can not be null',
            'form_meta': None
        })
    (form_meta, err) = form_meta_controller.find_form_meta(name, version)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    if form_meta is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'form_meta': None
        }), 404
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
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    if form_meta is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'form_meta': None
        }), 404
    (_, err) = form_meta_controller.delete_form_meta({'name': name})
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>', methods=['PUT'])
def change_form_meta(name):
    (ifSuccessful, err) = form_meta_controller.update_form_meta(name, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }), 200

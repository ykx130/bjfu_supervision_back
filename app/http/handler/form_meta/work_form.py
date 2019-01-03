from flask import jsonify, request
from app.http.handler.form_meta import form_meta_blueprint
from app.core.controllers import form_meta_controller


@form_meta_blueprint.route('/work_forms', methods=['GET'])
def find_work_forms():
    (work_forms, num, err) = form_meta_controller.find_work_forms(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'work_forms': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'total': num,
        'work_forms': work_forms,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_forms/<int:id>', methods=['GET'])
def find_work_form(id):
    (work_form, err) = form_meta_controller.find_work_form(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'work_form': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'work_form': work_form,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_forms', methods=['POST'])
def insert_work_form():
    (ifSuccess, err) = form_meta_controller.insert_work_form(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_forms/<int:id>', methods=['DELETE'])
def delete_work_form(id):
    (ifSuccess, err) = form_meta_controller.delete_work_form(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_forms/<int:id>', methods=['PUT'])
def update_work_form(id):
    (ifSuccess, err) = form_meta_controller.update_work_form(id, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200

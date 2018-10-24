from app.http.handler.consult import consult_blueprint
from flask import request, jsonify
from app.core.controllers import consult_controller


@consult_blueprint.route('/consults', methods=['POST'])
def new_consult():
    (ifSuccess, err) = consult_controller.insert_consult(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult': None
    }), 200


@consult_blueprint.route('/consults')
def get_consults():
    (consults, total, err) = consult_controller.find_consults(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consults': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'total': total,
        'consults': consults
    }), 200


@consult_blueprint.route('/consults/<int:id>')
def get_consult(id):
    (consult, err) = consult_controller.find_consult(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consults': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult': consult
    }), 200


@consult_blueprint.route('/consults/<int:id>', methods=['DELETE'])
def del_consult(id):
    (ifSuccess, err) = consult_controller.delete_consult(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult': None
    }), 200


@consult_blueprint.route('/consults/<int:id>', methods=['PUT'])
def change_consult(id):
    (ifSuccess, err) = consult_controller.update_consult(id, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult': None,
        }), err.status_code
    return jsonify({
        'code': '200',
        'message': '',
        'consult': None
    }), 200


@consult_blueprint.route('/consult_types', methods=['POST'])
def new_consult_type():
    (ifSuccess, err) = consult_controller.insert_consult_type(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult_type': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult_type': None
    }), 200


@consult_blueprint.route('/consult_types')
def get_consult_types():
    (consult_types, total, err) = consult_controller.find_consult_types(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult_types': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult_types': consult_types,
        'total': total
    }), 200


@consult_blueprint.route('/consult_types/<int:id>')
def get_consult_type(id):
    (consult_type, err) = consult_controller.find_consult_type(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult_type': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult_type': consult_type
    }), 200


@consult_blueprint.route('/consult_types/<int:id>', methods=['DELETE'])
def del_consult_type(id):
    (ifSuccess, err) = consult_controller.delete_consult_type(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult_type': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'consult_type': None
    }), 200


@consult_blueprint.route('/consult_types/<int:id>', methods=['PUT'])
def change_consult_type(id):
    (ifSuccess, err) = consult_controller.update_consult_type(id, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'consult_type': None,
        }), err.status_code
    return jsonify({
        'code': '200',
        'message': '',
        'consult_type': None
    }), 200

from app.http.handler.consult import consult_blueprint
from flask import request, jsonify
from app.core.controllers import consult_controller


@consult_blueprint.route('/consults', methods=['POST'])
def new_consult():
    (ifSuccess, err) = consult_controller.insert_consult(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult': None
        }), 500 if type(err) is not str else 200
    return jsonify({
        'code': 200,
        'message': '',
        'consult': None
    })


@consult_blueprint.route('/consults')
def get_consults():
    (consults, total, err) = consult_controller.find_consults(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'total': 0,
            'message': str(err),
            'consults': []
        })
    else:
        return jsonify({
            'code': 200,
            'message': '',
            'total': total,
            'consults': consults
        })


@consult_blueprint.route('/consults/<int:id>')
def get_consult(id):
    (consult, err) = consult_controller.find_consult(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult': None
        }), 500 if type(err) is not str else 200
    if consult is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'consult': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'consult': consult
    })


@consult_blueprint.route('/consults/<int:id>', methods=['DELETE'])
def del_consult(id):
    (consult, err) = consult_controller.find_consult(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult': None
        }), 500 if type(err) is not str else 200
    if consult is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'consult': None
        }), 404
    (ifSuccess, err) = consult_controller.delete_consult(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult': None
        }), 500 if type(err) is not str else 200
    return jsonify({
        'code': 200,
        'message': '',
        'consult': None
    })


@consult_blueprint.route('/consults/<int:id>', methods=['PUT'])
def change_consult(id):
    (consult, err) = consult_controller.find_consult(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult': None
        }), 500 if type(err) is not str else 200
    if consult is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'consult': None
        }), 404
    (ifSuccess, err) = consult_controller.update_consult(id, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult': None
        })
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
            'code': 500,
            'message': str(err),
            'consult_type': None
        }), 500 if type(err) is not str else 200
    return jsonify({
        'code': 200,
        'message': '',
        'consult_type': None
    })


@consult_blueprint.route('/consult_types')
def get_consult_types():
    (consult_types, total, err) = consult_controller.find_consult_types(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult_types': []
        })
    else:
        return jsonify({
            'code': 200,
            'message': '',
            'consult_types': consult_types
        })


@consult_blueprint.route('/consult_types/<int:id>')
def get_consult_type(id):
    (consult_type, err) = consult_controller.find_consult_type(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult_type': None
        }), 500 if type(err) is not str else 200
    if consult_type is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'consult_type': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'consult_type': consult_type
    })


@consult_blueprint.route('/consult_types/<int:id>', methods=['DELETE'])
def del_consult_type(id):
    (consult_type, err) = consult_controller.find_consult_type(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult_type': None
        }), 500 if type(err) is not str else 200
    if consult_type is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'consult_type': None
        }), 404
    (ifSuccess, err) = consult_controller.delete_consult_type(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult_type': None
        }), 500 if type(err) is not str else 200
    return jsonify({
        'code': 200,
        'message': '',
        'consult_type': None
    })


@consult_blueprint.route('/consult_types/<int:id>', methods=['PUT'])
def change_consult_type(id):
    (consult_type, err) = consult_controller.find_consult_type(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult_type': None
        }), 500 if type(err) is not str else 200
    if consult_type is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'consult_type': None
        }), 404
    (ifSuccess, err) = consult_controller.update_consult_type(id, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'consult_type': None
        })
    return jsonify({
        'code': '200',
        'message': '',
        'consult_type': None
    }), 200

from app.http.handler.form import form_blueprint
from flask import jsonify, request
from app.core.controllers import form_controller
from flask_pymongo import ObjectId


@form_blueprint.route('/forms', methods=['POST'])
def new_form():
    (_, err) = form_controller.insert_form(request)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form': None
        })
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }), 200


@form_blueprint.route('/forms')
def get_forms():
    (forms, total, err) = form_controller.find_forms(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'forms': []
        }), 500
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
            'code': 500,
            'message': str(err),
            'form': None
        }), 500
    if form is None:
        return jsonify({
            'code': 404,
            "message": 'Not found',
            'form': None
        }), 404
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
            'code': 500,
            'message': str(err),
            'form': None
        }), 500
    if form is None:
        return jsonify({
            'code': 404,
            'message': "not found",
            'form': None
        }), 404
    (_, err) = form_controller.delete_form({'_id': ObjectId(_id)})
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    })


@form_blueprint.route('/forms/<string:_id>', methods=['PUT'])
def change_form(_id):
    (form, err) = form_controller.find_form(_id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form': None
        }), 500
    if form is None:
        return jsonify({
            'code': 404,
            'message': 'no this form',
            'form': None
        }), 404
    (_, err) = form_controller.update_form({'_id': ObjectId(_id)}, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }), 200

from app.http.handler.model_lesson import model_lesson_blueprint
from flask import request, jsonify
from app.core.controllers import model_lesson_controller


@model_lesson_blueprint.route('/model_lessons')
def find_model_lessons():
    (model_lessons, total, err) = model_lesson_controller.find_model_lessons(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'users': [],
            'total': 0
        }), 500
    return jsonify({
        'code': 200,
        'total': total,
        'model_lessons': model_lessons,
        'message': ''
    }), 200


@model_lesson_blueprint.route('/model_lessons', methods=['POST'])
def insert_model_lesson():
    (ifSuccess, err) = model_lesson_controller.insert_model_lesson(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'model_lesson': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    })


@model_lesson_blueprint.route('/model_lessons/batch', methods=['POST'])
def insert_model_lessons():
    (ifSuccess, err) = model_lesson_controller.insert_model_lessons(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'model_lesson': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    })


@model_lesson_blueprint.route('/model_lessons/<int:id>')
def find_model_lesson(id):
    (model_lesson, model_lesson_users, err) = model_lesson_controller.find_model_lesson(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'model_lesson': None
        }), 200 if type(err) is str else 500
    if model_lesson is None:
        return jsonify({
            'code': 404,
            'message': 'not found'
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': model_lesson,
        'model_lesson_users': model_lesson_users
    })


@model_lesson_blueprint.route('/model_lessons/<int:id>', methods=['DELETE'])
def delete_model_lesson(id):
    (ifSuccess, err) = model_lesson_controller.delete_model_lesson(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'model_lesson': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    })


@model_lesson_blueprint.route('/model_lessons', methods=['DELETE'])
def delete_model_lessons():
    (ifSuccess, err) = model_lesson_controller.delete_model_lessons(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'model_lesson': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    })


@model_lesson_blueprint.route('/model_lessons/<int:id>', methods=['PUT'])
def update_model_lesson(id):
    (ifSuccess, err) = model_lesson_controller.update_model_lesson(id, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'model_lesson': None
        }), 200 if type(err) is str else 500
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    })

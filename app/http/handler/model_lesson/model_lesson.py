from app.http.handler.model_lesson import model_lesson_blueprint
from flask import request, jsonify
from app.core.controllers import model_lesson_controller


@model_lesson_blueprint.route('/model_lessons')
def find_model_lessons():
    (model_lessons, total, err) = model_lesson_controller.find_model_lessons(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'model_lessons': None,
            'total': None
        }), err.status_code
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
            'code': err.code,
            'message': err.err_info,
            'model_lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    }), 200


@model_lesson_blueprint.route('/model_lessons/batch', methods=['POST'])
def insert_model_lessons():
    (ifSuccess, err) = model_lesson_controller.insert_model_lessons(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'model_lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    }), 200


@model_lesson_blueprint.route('/model_lessons/<int:id>')
def find_model_lesson(id):
    (model_lesson, err) = model_lesson_controller.find_model_lesson(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'model_lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': model_lesson
    }), 200


@model_lesson_blueprint.route('/model_lessons/<int:id>', methods=['DELETE'])
def delete_model_lesson(id):
    (ifSuccess, err) = model_lesson_controller.delete_model_lesson(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'model_lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    }), 200


@model_lesson_blueprint.route('/model_lessons', methods=['DELETE'])
def delete_model_lessons():
    (ifSuccess, err) = model_lesson_controller.delete_model_lessons(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'model_lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    }), 200


@model_lesson_blueprint.route('/model_lessons/<int:id>', methods=['PUT'])
def update_model_lesson(id):
    (ifSuccess, err) = model_lesson_controller.update_model_lesson(id, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'model_lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    }), 200


@model_lesson_blueprint.route('/model_lessons/<int:id>/vote', methods=['post'])
def model_lesson_vote(id):
    (ifSuccess, err) = model_lesson_controller.model_lesson_vote(id, request.json.get('vote', True))
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'model_lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'model_lesson': None
    }), 200


@model_lesson_blueprint.route('/model_lessons/excel/import', methods=['POST'])
def import_lesson_excel():
    (ifSuccess, err) = model_lesson_controller.import_lesson_excel(request)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'notice_lesson': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'notice_lesson': None
    }), 200


@model_lesson_blueprint.route('/model_lessons/excel/export', methods=['POST'])
def export_lesson_excel():
    (ifSuccess, err) = model_lesson_controller.export_lesson_excel(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'notice_lesson': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'notice_lesson': None
    }), 200

from app.http.handler.lesson import lesson_blueprint
from flask import jsonify, request
from app.utils.misc import convert_datetime_to_string
from app.core.controllers import lesson_controller
from app.utils.url_condition.url_condition_mongodb import dict_serializable


@lesson_blueprint.route('/lessons', methods=['POST'])
def new_lesson():
    lesson_controller.update_database()
    return jsonify({
        'code': 200,
        'message': '',
        'lesson': None
    }), 200


@lesson_blueprint.route('/lessons')
def get_lessons():
    (lessons, num, err) = lesson_controller.find_lessons(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'lessons': None,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lessons': lessons,
        'total': num,
    }), 200


@lesson_blueprint.route('/lessons/<string:lesson_id>')
def get_lesson(lesson_id):
    (lesson, err) = lesson_controller.find_lesson(lesson_id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'lesson': lesson
    }), 200


@lesson_blueprint.route('/lessons/<int:id>', methods=["PUT"])
def update_lesson(id):
    (_, err) = lesson_controller.change_lesson(id, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@lesson_blueprint.route('/terms')
def get_terms():
    (terms, total, err) = lesson_controller.find_terms(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'terms': terms,
        'total': total,
        'message': ''
    }), 200


@lesson_blueprint.route('/terms/current')
def get_term_now():
    (term, err) = lesson_controller.find_now_term()
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'lesson': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'term': term
    }), 200

from app.http.handler.lesson import lesson_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from app.utils.misc import convert_datetime_to_string
from flask import url_for
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from app.core.controllers.lesson_controller import update_database, find_lessons, find_lesson, find_now_term, \
    find_terms, change_lesson, has_lesson
from app.core.controllers.common_controller import dict_serializable, UrlCondition, Paginate, sort_limit


@lesson_blueprint.route('/lessons', methods=['POST'])
def new_lesson():
    update_database()
    return jsonify({
        'code': 200,
        'message': '',
        'lesson': None
    }), 200


@lesson_blueprint.route('/lessons')
def get_lessons():
    (lessons, num, err) = find_lessons(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'total': 0,
            'lessons': []
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'lessons': [dict_serializable(lesson) for lesson in lessons],
        'total': num,
    }), 200


@lesson_blueprint.route('/lessons/<int:id>')
def get_lesson(id):
    (lesson, err) = find_lesson(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'lesson': None
        }), 500
    if lesson is None:
        return jsonify({
            'code': 404,
            "message": 'Not found',
            'lesson': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'lesson': dict_serializable(lesson) if lesson is not None else None
    }), 200


@lesson_blueprint.route('/lessons/<int:id>', methods=["PUT"])
def update_lesson(id):
    (lesson, err) = find_lesson(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'lesson': None
        }), 500
    if lesson is None:
        return jsonify({
            'code': 404,
            "message": 'Not found',
            'lesson': None
        }), 404
    (_, err) = change_lesson(id, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'lesson': None
        }), 500
    return jsonify({
        'code': 202,
        'message': ''
    })


@lesson_blueprint.route('/terms')
def get_terms():
    (terms, total, err) = find_terms(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'terms': [],
            'total': 0
        }), 500
    return jsonify({
        'code': 200,
        'terms': [{
            'id': term.id,
            'name': term.name,
            'begin_time': convert_datetime_to_string(term.begin_time),
            'end_time': convert_datetime_to_string(term.end_time)
        } for term in terms],
        'total': total,
        'message': ''
    }), 200


@lesson_blueprint.route('/terms/current')
def get_term_now():
    (term, err) = find_now_term()
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'term': None
        }), 500
    if term is None:
        return jsonify({
            "code": 404,
            "message": "there is no term"
        }), 404
    return jsonify({
        'code': 200,
        'term': {
            'id': term.id,
            'name': term.name,
            'begin_time': convert_datetime_to_string(term.begin_time),
            'end_time': convert_datetime_to_string(term.end_time)
        }
    }), 200

from app.http.handler.lesson import lesson_blueprint
from flask_pymongo import ObjectId
from flask import jsonify, request
from flask import url_for
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from app.core.controllers.lesson_controller import update_database, find_lessons, find_lesson
from app.core.controllers.common_controller import dict_serializable, UrlCondition, Paginate, sort_limit


@lesson_blueprint.route('/lessons', methods=['POST'])
def new_lesson():
    from run import mongo
    try:
        update_database(mongo)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'lesson':None
        }),500
    return jsonify({
        'code':200,
        'message':'',
        'lesson':None
    }),200


@lesson_blueprint.route('/lessons')
def get_lessons():
    url_condition = UrlCondition(request.args)
    from run import mongo
    try:
        lessons = find_lessons(mongo, url_condition.filter_dict)
    except:
        return jsonify({
            'code':500,
            'message':'',
            'lessons':None
        }),500
    lessons = sort_limit(lessons, url_condition.sort_limit_dict)
    paginate = Paginate(lessons, url_condition.page_dict)
    return jsonify({
        'code': 200,
        'message': '',
        'lessons': [dict_serializable(lesson) for lesson in lessons],
        'total': paginate.total,
    }),200


@lesson_blueprint.route('/lessons/<string:_id>')
def get_lesson(_id):
    from run import mongo
    try:
        lesson = find_lesson(mongo, _id)
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'lesson':None
        }),500
    if lesson is None:
        return jsonify({
            'code':404,
            "message":'Not found',
            'lesson':None
        }),404
    return jsonify({
        'code':200,
        'message':'',
        'lesson':dict_serializable(lesson) if lesson is not None else None
    }),200
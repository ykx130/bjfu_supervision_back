from app.http.handler.notices import notices_blueprint
from flask_pymongo import ObjectId
from flask_login import current_user
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from app.utils.misc import convert_datetime_to_string
from flask import url_for
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from app.core.controllers.lesson_controller import update_database, find_lessons, find_lesson, find_now_term, \
    find_terms, change_lesson, has_lesson
from app.core.controllers import notices_controller


@notices_blueprint.route('/notices')
def get_notices_num():
    num = notices_controller.get_notices_num(current_user.username)
    return jsonify({
        "code": 200,
        "total": num
    })


@notices_blueprint.route('/notices/newest')
def get_newest_notice():
    notice = notices_controller.get_newest_notices(current_user.username)
    return jsonify({
        "code": 200,
        "notice": notice
    })

from flask import Blueprint

notice_lesson_blueprint = Blueprint('notice_lesson_blueprint', __name__)

from . import notice_lesson

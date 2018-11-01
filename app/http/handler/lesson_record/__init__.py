from flask import Blueprint

lesson_record_blueprint = Blueprint('lesson_record_blueprint', __name__)

from . import lesson_record

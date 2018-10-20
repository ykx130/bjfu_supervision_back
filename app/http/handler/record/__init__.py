from flask import Blueprint

lesson_records_blueprint = Blueprint('lesson_records_blueprint', __name__)

from . import lesson_record

from flask import Blueprint

model_lesson_blueprint = Blueprint('model_lesson_blueprint', __name__)

from . import model_lesson

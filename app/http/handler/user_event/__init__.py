from flask import Blueprint

user_event_blueprint = Blueprint('user_event_blueprint', __name__)

from . import user_event
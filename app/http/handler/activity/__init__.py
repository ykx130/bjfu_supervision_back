from flask import Blueprint

activity_blueprint = Blueprint('activity_blueprint', __name__)

from . import activity

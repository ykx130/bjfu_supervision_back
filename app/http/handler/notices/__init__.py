from flask import Blueprint

notices_blueprint = Blueprint('notices_blueprint', __name__)

from . import notices

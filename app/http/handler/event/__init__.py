from flask import Blueprint

event_blueprint = Blueprint('event_blueprint', __name__)

from . import event
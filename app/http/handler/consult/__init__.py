from flask import Blueprint

consult_blueprint = Blueprint('consult_blueprint', __name__)

from . import consult

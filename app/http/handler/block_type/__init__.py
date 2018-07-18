from flask import Blueprint

block_type_blueprint = Blueprint('block_type_blueprint', __name__)

from . import block_type
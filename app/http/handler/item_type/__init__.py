from flask import Blueprint

item_type_blueprint = Blueprint('item_type_blueprint', __name__)

from . import item_type
from flask import Blueprint

page_data_blueprint = Blueprint('page_data_blueprint', __name__)

from . import page_data

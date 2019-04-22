from flask import Blueprint

form_blueprint = Blueprint('form_blueprint', __name__)
form_meta_blueprint = Blueprint('form_meta_blueprint', __name__)
activity_blueprint = Blueprint('activity_blueprint', __name__)
user_blueprint = Blueprint('user_blueprint', __name__)

from . import form, form_meta, work_plan, activity, user, auth

from flask import Blueprint

activity_blueprint = Blueprint('activity_blueprint', __name__)
form_blueprint = Blueprint('form_blueprint', __name__)
form_meta_blueprint = Blueprint('form_meta_blueprint', __name__)
user_blueprint = Blueprint('user_blueprint', __name__)
consult_blueprint = Blueprint('consult_blueprint', __name__)
event_blueprint = Blueprint('event_blueprint', __name__)
lesson_blueprint = Blueprint('lesson_blueprint', __name__)
lesson_record_blueprint = Blueprint('lesson_record_blueprint', __name__)
model_lesson_blueprint = Blueprint('model_lesson_blueprint', __name__)
other_model_lesson_blueprint=Blueprint('other_model_lesson_blueprint', __name__)
notice_lesson_blueprint = Blueprint('notice_lesson_blueprint', __name__)
notices_blueprint = Blueprint('notices_blueprint', __name__)
page_data_blueprint = Blueprint('page_data_blueprint', __name__)
captcha_bp = Blueprint('captcha_blueprint', __name__)


from . import activity, auth, consult, event, form, form_meta, lesson, lesson_record, model_lesson, notice_lesson, \
    notices,other_model_lesson, user, work_plan, captcha_bp

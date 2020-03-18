from app.http.handler import other_model_lesson_blueprint
from flask import request, jsonify
import app.core.controller as controller
from flask_login import login_required
from app.http.handler.filter import Filter
from app.utils import CustomError, args_to_dict, db

@other_model_lesson_blueprint.route('/other_model_lessons')
@login_required
@Filter.filter_permission()
def find_other_model_lessons(*args,**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    print(query_dict)
    try:
        (other_model_lessons,total) = controller.OtherModelLessonController.query_other_model_lessons(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
         'total': total,
        'other_model_lessons': other_model_lessons,
        'msg': ''
    }), 200
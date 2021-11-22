from app.http.handler import activity_blueprint
from flask import request, jsonify
from flask_login import login_required
import app.core.controller  as controller
from flask_login import current_user
from app.utils import CustomError, args_to_dict, db
from app.http.handler.filter import Filter


@activity_blueprint.route('/activities')
@login_required
def find_activities(**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (activities, total) = controller.ActivityController.query_activities(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'activities': activities,
        'msg': ''
    }), 200


@activity_blueprint.route('/activities', methods=['POST'])
@login_required
def insert_activity(**kwargs):
    try:
        controller.ActivityController.insert_activity(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200

@activity_blueprint.route('/acyivities/excel/import', methods=['POST'])
@login_required
def import_activitys_excel():
    try:
        path = controller.ActivityController.import_activity_excel(data=request)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    if path is None:
        return jsonify({
            'code': 200,
            'msg': '',
            'fail_excel_path': path
        }), 200
    else:
        return jsonify({
            'code': 500,
            'msg': '',
            'fail_excel_path': path
        }), 200


@activity_blueprint.route('/activities/<int:id>')
@login_required
def find_activity(id, *args, **kwargs):
    try:
        query_dict = {}
        query_dict.update(kwargs)
        query_dict.update({'id': id})
        activity = controller.ActivityController.get_activity(query_dict={'id': id})
        # (activity_users, num) = controller.ActivityUserController.query_activity_users(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity': activity,
        # 'activity_users': activity_users
    }), 200


@activity_blueprint.route('/activities/<int:id>', methods=['DELETE'])
@login_required
def delete_activity(id, **kwargs):
    try:
        controller.ActivityController.delete_activity(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>', methods=['PUT'])
@login_required
def update_activity(id, **kwargs):
    try:
        controller.ActivityController.update_activity(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users')
@login_required
def find_activity_users(id, **kwargs):
    try:
        query_dict = {}
        query_dict.update(args_to_dict(request.args))
        query_dict.update(kwargs)
        activity = controller.ActivityController.get_activity(query_dict={'id': id})
        query_dict.update({'activity_id':id})
        (activity_users, total) = controller.ActivityUserController.query_activity_users(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity': activity,
        'activity_users': activity_users
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users', methods=['POST'])
@login_required
def insert_activity_user(id, **kwargs):
    try:
        controller.ActivityUserController.insert_activity_user(activity_id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200

@activity_blueprint.route('/activities/activity_users_apply/<string:username>', methods=['POST'])
@login_required
def insert_activity_user_apply(username,**kwargs):
    try:
        controller.ActivityUserController.insert_activity_user_apply(username=username, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200

@activity_blueprint.route('/activities/activity_users_excel/import', methods=['POST'])
@login_required
def import_activitys_user_excel(**kwargs):
    try:
        path = controller.ActivityUserController.import_activity_user_excel(data=request)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    if path is None:
        return jsonify({
            'code': 200,
            'msg': '',
            'fail_excel_path': path
        }), 200
    else:
        return jsonify({
            'code': 500,
            'msg': '',
            'fail_excel_path': path
        }), 200

@activity_blueprint.route('/activities/activity_users_excel/export', methods=['POST'])
@login_required
def export_activity_users_excel():
    try:
        filename = controller.ActivityUserController.export_activity_user(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'filename': filename
    }), 200


@activity_blueprint.route('/activities/competition_users_excel/import', methods=['POST'])
@login_required
def import_competition_users_excel(**kwargs):
    try:
        path = controller.ActivityUserController.import_competition_user_excel(data=request)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    if path is None:
        return jsonify({
            'code': 200,
            'msg': '',
            'fail_excel_path': path
        }), 200
    else:
        return jsonify({
            'code': 500,
            'msg': '',
            'fail_excel_path': path
        }), 200

@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>')
@login_required
def find_activity_user(id, username, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        activity = controller.ActivityController.get_activity(query_dict=query_dict)
        activity_user = controller.ActivityUserController.get_activity_user(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity': activity,
        'activity_users': activity_user
    }), 200


@activity_blueprint.route('/activities/activity_users', methods=['DELETE'])
@login_required
def delete_activity_user():
    try:
        query_dict = {}
        query_dict.update(args_to_dict(request.args))
        controller.ActivityUserController.delete_activity_user(data=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200


@activity_blueprint.route('/activities/<int:id>/activity_users/<string:username>', methods=['PUT'])
@login_required
def update_activity_user(id, username, **kwargs):
    try:
        controller.ActivityUserController.update_activity_user(activity_id=id, username=username, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200

@activity_blueprint.route('/activities/<int:id>/batch_update_activity_users_state', methods=['PUT'])
@login_required
def batch_update_activity_users_state(id, **kwargs):
    try:
        controller.ActivityUserController.batch_update_activity_user_state(activity_id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': ''
    }), 200   

@activity_blueprint.route('/current_user/activities')
@login_required
def get_current_user_activities(**kwargs):
    username = request.args['username'] if 'username' in request.args else current_user.username
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (activities, total) = controller.ActivityUserController.query_current_user_activities(username=username,
                                                                                              query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'total': total,
        'activities': activities
    }), 200

@activity_blueprint.route('/activities/activity_users')
@login_required
def get_activity_users(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (activity_users, total) = controller.ActivityUserController.query_activity_users(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'activity_users': activity_users,
        'msg': ''
    }), 200


@activity_blueprint.route('/competition')
@login_required
def find_competitions(**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (competitions, total) = controller.CompetitionController.query_competitions(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'competitions': competitions,
        'msg': ''
    }), 200


@activity_blueprint.route('/competition', methods=['POST'])
@login_required
def insert_competition(**kwargs):
    try:
        controller.CompetitionController.insert_competition(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200



@activity_blueprint.route('/competition/<int:id>')
@login_required
def find_competition(id, *args, **kwargs):
    try:
        query_dict = {}
        query_dict.update(kwargs)
        query_dict.update({'id': id})
        competition = controller.CompetitionController.get_competition(query_dict={'id': id})
        (activity_users, num) = controller.ActivityUserController.query_activity_users(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'competition': competition,
        'activity_users': activity_users
    }), 200


@activity_blueprint.route('/competition/<int:id>', methods=['DELETE'])
@login_required
def delete_competition(id, **kwargs):
    try:
        controller.CompetitionController.delete_competition(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/competition/<int:id>', methods=['PUT'])
@login_required
def update_competition(id, **kwargs):
    try:
        controller.CompetitionController.update_competition(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200



@activity_blueprint.route('/exchange')
@login_required
def find_exchanges(**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (exchanges, total) = controller.ExchangeController.query_exchanges(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'exchanges': exchanges,
        'msg': ''
    }), 200


@activity_blueprint.route('/exchange', methods=['POST'])
@login_required
def insert_exchange(**kwargs):
    try:
        controller.ExchangeController.insert_exchange(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200



@activity_blueprint.route('/exchange/<int:id>')
@login_required
def find_exchange(id, *args, **kwargs):
    try:
        query_dict = {}
        query_dict.update(kwargs)
        query_dict.update({'id': id})
        exchange = controller.ExchangeController.get_exchange(query_dict={'id': id})
        (activity_users, num) = controller.ActivityUserController.query_activity_users(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'exchange': exchange,
        'activity_users': activity_users
    }), 200


@activity_blueprint.route('/exchange/<int:id>', methods=['DELETE'])
@login_required
def delete_exchange(id, **kwargs):
    try:
        controller.ExchangeController.delete_exchange(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/exchange/<int:id>', methods=['PUT'])
@login_required
def update_exchange(id, **kwargs):
    try:
        controller.ExchangeController.update_exchange(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200



@activity_blueprint.route('/research')
@login_required
def find_researchs(**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (researchs, total) = controller.ResearchController.query_researchs(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'researchs': researchs,
        'msg': ''
    }), 200


@activity_blueprint.route('/research', methods=['POST'])
@login_required
def insert_research(**kwargs):
    try:
        controller.ResearchController.insert_research(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200



@activity_blueprint.route('/research/<int:id>', methods=['DELETE'])
@login_required
def delete_research(id, **kwargs):
    try:
        controller.ResearchController.delete_research(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/research/<int:id>', methods=['PUT'])
@login_required
def update_research(id, **kwargs):
    try:
        controller.ResearchController.update_research(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200

@activity_blueprint.route('/project')
@login_required
def find_projects(**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (projects, total) = controller.ProjectController.query_projects(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'projects': projects,
        'msg': ''
    }), 200


@activity_blueprint.route('/project', methods=['POST'])
@login_required
def insert_project(**kwargs):
    try:
        controller.ProjectController.insert_project(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200



@activity_blueprint.route('/project/<int:id>', methods=['DELETE'])
@login_required
def delete_project(id, **kwargs):
    try:
        controller.ProjectController.delete_project(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/project/<int:id>', methods=['PUT'])
@login_required
def update_project(id, **kwargs):
    try:
        controller.ProjectController.update_project(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200

@activity_blueprint.route('/activities_plan/<int:id>', methods=['PUT'])
@login_required
def update_activity_plan(id, **kwargs):
    try:
        controller.ActivityPlanController.update_activity_plan(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200

@activity_blueprint.route('/activities/activity_plans')
@login_required
def get_activity_plans(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (activity_plans, total) = controller.ActivityPlanController.query_activity_plans(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'activity_plans': activity_plans,
        'msg': ''
    }), 200

@activity_blueprint.route('/activities/user_plan/<string:username>')
@login_required
def get_user_plan(username, **kwargs):
    try:
        user_plan_data = controller.ActivityPlanController.get_user_plan(username=username)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'user_plan_data': user_plan_data
    }), 200


@activity_blueprint.route('/activities/plan_file/upload', methods=['POST'])
@login_required
def upload_planfile():
    try:
        path = controller.FileRecordController.uploadplanfile(data=request)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    if path is None:
        return jsonify({
            'code': 200,
            'msg': ''
        }), 200
    else:
        return jsonify({
            'code': 500,
            'msg': 'success'
        }), 200


@activity_blueprint.route('/activities/pic_file/upload', methods=['POST'])
@login_required
def upload_pic_file():
    try:
        path = controller.FileRecordController.uploadpic(data=request)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    if path is None:
        return jsonify({
            'code': 200,
            'msg': ''
        }), 200
    else:
        return jsonify({
            'code': 500,
            'msg': 'success',
            'path':path
        }), 200

# 返回上传的活动文件的路径
@activity_blueprint.route('/activities/file/upload', methods=['POST'])
@login_required
def upload_activity_file():
    try:
        path = controller.FileRecordController.upload_activityfile(data=request)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    if path is None:
        return jsonify({
            'code': 200,
            'msg': ''
        }), 200
    else:
        return jsonify({
            'code': 500,
            'msg': 'success',
            'path':path
        }), 200

@activity_blueprint.route('/activities/planfile/export/<string:filename>', methods=['POST'])
@login_required
def export_planfile(filename, **kwargs):
    try:
        filename=controller.FileRecordController.download_file(filename=filename)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'filename':filename
    }), 200

@activity_blueprint.route('/activities/query_files')
@login_required
def query_files(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (files, total) = controller.FileRecordController.query_files(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'files': files,
        'msg': ''
    }), 200

@activity_blueprint.route('/activities/users_score')
@login_required
def query_users_score(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (users_score, total) = controller.ActivityUserScoreController.query_users_score(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': total,
        'users_score': users_score,
        'msg': ''
    }), 200

@activity_blueprint.route('/insert_activity_module', methods=['POST'])
@login_required
def insert_activity_module():
    try:
        controller.ActivityModuleController.insert_activity_modules(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/activity_modules')
@login_required
def query_activity_modules(*args, **kwargs):
    try:
        query_dict = {}
        query_dict.update(args_to_dict(request.args))
        query_dict.update(kwargs)
        (activity_modules, total) = controller.ActivityModuleController.query_activity_modules(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity_modules': activity_modules,
        'total': total
    }), 200


@activity_blueprint.route('/activity_module/<int:id>')
@login_required
def get_activity_module_by_id(id):
    try:
        activity_module = controller.ActivityModuleController.get_activity_module(query_dict={'id': id}, unscoped=False)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'activity_module': activity_module
    }), 200


@activity_blueprint.route('/update_activity_module/<int:id>', methods=['PUT'])
@login_required
def update_activity_module(id, **kwargs):
    try:
        controller.ActivityModuleController.update_activity_modules(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@activity_blueprint.route('/delete_activity_module/<int:id>', methods=['DELETE'])
@login_required
def delete_activity_module(id, **kwargs):
    try:
        controller.ActivityModuleController.delete_activity_modules(id=id)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200

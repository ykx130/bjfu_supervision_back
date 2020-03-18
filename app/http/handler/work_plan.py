from flask import jsonify, request
from app.http.handler import form_meta_blueprint
import app.core.controller as controller
from app.utils import args_to_dict, CustomError, db
from app.http.handler.filter import Filter
from flask_login import login_required


@form_meta_blueprint.route('/work_plans', methods=['GET'])
@login_required
def find_work_plans(**kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (work_plans, num) = controller.WorkPlanController.query_work_plan(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': num,
        'work_plans': work_plans,
        'msg': ''
    }), 200


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['GET'])
@login_required
def find_work_plan(id, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        query_dict = kwargs
        query_dict.update({'id': id})
        work_plan = controller.WorkPlanController.get_work_plan(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'work_plan': work_plan,
        'msg': ''
    }), 200


@form_meta_blueprint.route('/work_plans', methods=['POST'])
@login_required
def insert_work_plan():

    try:
        controller.WorkPlanController.insert_work_plan(data=request.json)
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


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['DELETE'])
@login_required
def delete_work_plan(id):
    try:
        controller.WorkPlanController.delete_work_plan(id=id)
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


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['PUT'])
@login_required
def update_work_plan(id):
    try:
        controller.WorkPlanController.update_work_plan(id=id, data=request.json)
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


@form_meta_blueprint.route('/work_plan/details/<string:term>', methods=['GET'])
@login_required
@Filter.filter_permission()
def find_work_plans_detail(term, *args, **kwargs):
    query_dict = kwargs
    query_dict.update({'term':term})
    try:
        (work_plans, total) = controller.WorkPlanController.query_work_plan_detail(query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'work_plans': work_plans,
        'total': total
    }), 200

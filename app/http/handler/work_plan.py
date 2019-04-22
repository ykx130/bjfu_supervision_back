from flask import jsonify, request
from app.http.handler import form_meta_blueprint
import app.core.controller as controller
from app.utils import args_to_dict, CustomError


@form_meta_blueprint.route('/work_plans', methods=['GET'])
def find_work_plans():
    try:
        (work_plans, num) = controller.WorkPlanController.query_work_plan(query_dict=args_to_dict(request.args))
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'total': num,
        'work_plans': work_plans,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['GET'])
def find_work_plan(id):
    try:
        work_plan = controller.WorkPlanController.get_work_plan(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'work_plan': work_plan,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans', methods=['POST'])
def insert_work_plan():
    try:
        controller.WorkPlanController.insert_work_plan(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['DELETE'])
def delete_work_plan(id):
    try:
        controller.WorkPlanController.delete_work_plan(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['PUT'])
def update_work_plan(id):
    try:
        controller.WorkPlanController.update_work_plan(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'message': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200

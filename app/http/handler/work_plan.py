from flask import jsonify, request
from app.http.handler import form_meta_blueprint
import app.core.controllers as core


@form_meta_blueprint.route('/work_plans', methods=['GET'])
def find_work_plans():
    (work_plans, num, err) = core.WorkPlanController.query_work_plan(request.args)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'work_plans': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'total': num,
        'work_plans': work_plans,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['GET'])
def find_work_plan(id):
    (work_plan, err) = core.WorkPlanController.get_work_plan(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'work_plan': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'work_plan': work_plan,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans', methods=['POST'])
def insert_work_plan():
    (ifSuccess, err) = core.WorkPlanController.insert_work_plan(request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['DELETE'])
def delete_work_plan(id):
    (ifSuccess, err) = core.WorkPlanController.delete_work_plan(id)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plans/<int:id>', methods=['PUT'])
def update_work_plan(id):
    (ifSuccess, err) = core.WorkPlanController.update_work_plan(id, request.json)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': ''
    }), 200


@form_meta_blueprint.route('/work_plan/details/<string:term>', methods=['GET'])
def find_work_plans_detail(term):
    (work_plans, total, err) = form_meta_controller.find_work_plan_detail(term)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'total': None
        }), err.status_code
    return jsonify({
        'code': 200,
        'work_plans': work_plans,
        'total': total
    }), 200

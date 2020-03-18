from app.http.handler import event_blueprint
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError, args_to_dict, db
from flask_login import login_required
from app.http.handler.filter import Filter


@event_blueprint.route('/events', methods=['POST'])
@login_required
def new_event():
    try:
        controller.EventController.insert_event(data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    })


@event_blueprint.route('/events')
@login_required
def get_events(*args, **kwargs):
    query_dict = {}
    query_dict.update(args_to_dict(request.args))
    query_dict.update(kwargs)
    try:
        (events, total) = controller.EventController.query_events(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'events': events,
        'total': total
    }), 200


@event_blueprint.route('/users/<string:username>/events')
@login_required
def get_user_events(username, *args, **kwargs):
    query_dict = kwargs
    query_dict.update({'username': username})
    try:
        (events, total) = controller.EventController.query_user_events(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'events': events,
        'total': total
    }), 200


@event_blueprint.route('/events/<int:id>')
@login_required
def get_user(id, *args, **kwargs):
    query_dict = kwargs
    query_dict.update({'id': id})
    try:
        event = controller.EventController.get_event(query_dict=query_dict)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'event': event
    }), 200


@event_blueprint.route('/events/<int:id>', methods=['DELETE'])
@login_required
def del_event(id):
    try:
        controller.EventController.delete_event(id=id)
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


@event_blueprint.route('/events/<int:id>', methods=['PUT'])
@login_required
def change_event(id):
    try:
        controller.EventController.update_event(id=id, data=request.json)
    except CustomError as e:
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': '200',
        'msg': '',
    }), 200

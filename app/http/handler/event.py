from app.http.handler import event_blueprint
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError, args_to_dict


@event_blueprint.route('/events', methods=['POST'])
def new_event():
    try:
        controller.EventController.insert_event(data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    })


@event_blueprint.route('/events')
def get_events():
    try:
        (events, total) = controller.EventController.query_events(query_dict=args_to_dict(request.args))
    except CustomError as e:
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
def get_user_events(username):
    try:
        (events, total) = controller.EventController.query_user_events(username=username,
                                                                       query_dict=args_to_dict(request.args))
    except CustomError as e:
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
def get_user(id):
    try:
        event = controller.EventController.get_event(id=id)
    except CustomError as e:
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
def del_event(id):
    try:
        controller.EventController.delete_event(id=id)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
    }), 200


@event_blueprint.route('/events/<int:id>', methods=['PUT'])
def change_event(id):
    try:
        controller.EventController.update_event(id=id, data=request.json)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': '200',
        'msg': '',
    }), 200

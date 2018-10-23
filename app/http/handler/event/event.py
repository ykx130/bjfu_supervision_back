from app.http.handler.event import event_blueprint
from flask import request, jsonify
from app.core.controllers import event_controller


@event_blueprint.route('/events', methods=['POST'])
def new_event():
    (ifSuccess, err) = event_controller.insert_event(request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'event': None
        }), 500 if type(err) is not str else 200
    return jsonify({
        'code': 200,
        'message': '',
        'event': None
    })


@event_blueprint.route('/events')
def get_events():
    (events, total, err) = event_controller.find_events(request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'events': []
        })
    else:
        return jsonify({
            'code': 200,
            'message': '',
            'events': events,
            'total':total
        })


@event_blueprint.route('/users/<string:username>/events')
def get_user_events(username):
    (events, total, err) = event_controller.find_user_events(username, request.args)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'events': []
        })
    else:
        return jsonify({
            'code': 200,
            'message': '',
            'events': events,
            'total': total
        })


@event_blueprint.route('/events/<int:id>')
def get_user(id):
    (event, err) = event_controller.find_event(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'event': None
        }), 500 if type(err) is not str else 200
    if event is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'event': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'event': event
    })


@event_blueprint.route('/events/<int:id>', methods=['DELETE'])
def del_event(id):
    (event, err) = event_controller.find_event(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'event': None
        }), 500 if type(err) is not str else 200
    if event is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'event': None
        }), 404
    (ifSuccess, err) = event_controller.delete_event(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'event': None
        }), 500 if type(err) is not str else 200
    return jsonify({
        'code': 200,
        'message': '',
        'event': None
    })


@event_blueprint.route('/events/<int:id>', methods=['PUT'])
def change_event(id):
    (event, err) = event_controller.find_event(id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'event': None
        }), 500 if type(err) is not str else 200
    if event is None:
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'event': None
        }), 404
    (ifSuccess, err) = event_controller.update_event(id, request.json)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'event': None
        })
    return jsonify({
        'code': '200',
        'message': '',
        'event': None
    }), 200

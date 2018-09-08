from app.core.models.user import User, Event
from app import db


def find_events(condition):
    try:
        events = Event.events(condition)
    except Exception as e:
        return None, None, e
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = events.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def event_to_dict(event):
    return {
        'id': event.id,
        'username': event.username,
        'detail': event.detail,
        'timestamp': event.timestamp,
        'using': event.using
    }


def insert_event(request_json):
    event = Event()
    if 'username' not in request_json:
        return False, 'username can not be empty'
    for key, value in request_json.items():
        if hasattr(event, key):
            setattr(event, key, value)
    db.session.add(event)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def find_event(id):
    try:
        event = Event.query.filter(Event.id == int(id)).filter(Event.using == True).first()
    except Exception as e:
        return None, e
    if event is None:
        return None, None
    return event, None


def delete_event(id):
    try:
        event = Event.query.filter(Event.id == int(id)).filter(Event.using == True).first()
    except Exception as e:
        return False, e
    if event is None:
        return False, None
    event.using = False
    db.session.add(event)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def update_event(id, request_json):
    try:
        event = Event.query.filter(Event.id == int(id)).filter(Event.using == True).first()
    except Exception as e:
        return False, e
    if event is None:
        return False, None
    for key, value in request_json.items():
        if hasattr(event, key):
            setattr(event, key, value)
    db.session.add(event)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None

from app.core.models.user import User, Event
from app.utils.mysql import db
from app.utils.Error import CustomError


def find_events(condition):
    try:
        events = Event.events(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page'][0]) if '_page' in condition else 1
    per_page = int(condition['_per_page'][0]) if '_per_page' in condition else 20
    pagination = events.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def event_to_dict(event):
    try:
        event_dict = {
            'id': event.id,
            'username': event.username,
            'detail': event.detail,
            'timestamp': str(event.timestamp),
            'using': event.using
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return event_dict, None


def insert_event(request_json):
    event = Event()
    if 'username' not in request_json:
        return False, CustomError(500, 200, 'username can not be empty')
    for key, value in request_json.items():
        if hasattr(event, key):
            setattr(event, key, value)
    db.session.add(event)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def find_event(id):
    try:
        event = Event.query.filter(Event.id == int(id)).filter(Event.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if event is None:
        return None, CustomError(404, 404, 'event not found')
    return event, None


def delete_event(id):
    try:
        event = Event.query.filter(Event.id == int(id)).filter(Event.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if event is None:
        return False, CustomError(404, 404, 'event not found')
    event.using = False
    db.session.add(event)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_event(id, request_json):
    try:
        event = Event.query.filter(Event.id == int(id)).filter(Event.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if event is None:
        return False, CustomError(404, 404, 'event not found')
    for key, value in request_json.items():
        if hasattr(event, key):
            setattr(event, key, value)
    db.session.add(event)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None

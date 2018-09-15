from app.core.services import event_service


def find_events(condition):
    (events, num, err) = event_service.find_events(condition)
    if err is not None:
        return [], 0, err
    events_model = [event_service.event_to_dict(event) for event in events]
    return events_model, num, err


def insert_event(request_json):
    (ifSuccess, err) = event_service.insert_event(request_json)
    return ifSuccess, err


def find_event(id):
    (event, err) = event_service.find_event(id)
    if err is not None:
        return None, err
    event_model = event_service.event_to_dict(event)
    return event_model, err


def delete_event(id):
    (ifSuccess, err) = event_service.delete_event(id)
    return ifSuccess, err


def update_event(id, request_json):
    (ifSuccess, err) = event_service.update_event(id, request_json)
    return ifSuccess, err

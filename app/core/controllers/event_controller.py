from app.core.services import event_service
from app.utils.url_condition.url_args_to_dict import args_to_dict


def find_user_events(username, condition):
    condition_fin = args_to_dict(condition)
    if 'username' in condition_fin:
        condition_fin['username'].append(username)
    else:
        condition_fin['username'] = [username]
    (events, num, err) = event_service.find_events(condition_fin)
    if err is not None:
        return None, None, err
    events_model = list()
    for event in events:
        (event_model, err) = event_service.event_to_dict(event)
        if err is not None:
            return None, None, err
        events_model.append(event_model)
    return events_model, num, None


def find_events(condition):
    condition_fin = args_to_dict(condition)
    (events, num, err) = event_service.find_events(condition_fin)
    if err is not None:
        return None, None, err
    events_model = list()
    for event in events:
        (event_model, err) = event_service.event_to_dict(event)
        if err is not None:
            return None, None, err
        events_model.append(event_model)
    return events_model, num, None


def insert_event(request_json):
    (ifSuccess, err) = event_service.insert_event(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_event(id):
    (event, err) = event_service.find_event(id)
    if err is not None:
        return None, err
    (event_model, err) = event_service.event_to_dict(event)
    if err is not None:
        return None, err
    return event_model, None


def delete_event(id):
    (ifSuccess, err) = event_service.delete_event(id)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_event(id, request_json):
    (ifSuccess, err) = event_service.update_event(id, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None

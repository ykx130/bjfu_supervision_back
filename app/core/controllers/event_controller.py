from app.core.services import event_service


def find_user_events(username, condition):
    filter_dict = dict()
    for key, value in condition.items():
        filter_dict[key] = value
    filter_dict['username'] = username
    (events, num, err) = event_service.find_events(filter_dict)
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
    (events, num, err) = event_service.find_events(condition)
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

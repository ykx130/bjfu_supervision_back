from app.core.services import activity_service


def insert_activity(request_json):
    (ifSuccess, err) = activity_service.insert_activity(request_json)
    return ifSuccess, err


def update_activity(id, request_json):
    (ifSuccess, err) = activity_service.update_activity(id, request_json)
    return ifSuccess, err


def delete_activity(id):
    (ifSuccess, err) = activity_service.delete_activity(id)
    return ifSuccess, err


def activity_dict(activity):
    return activity_service.activity_dict(activity)


def activity_user_dict(id, user):
    return activity_service.activity_user_dict(id, user)


def find_activities(condition):
    (activities, num, err) = activity_service.find_activities(condition)
    if err is not None:
        return None, None, err
    activity_models = [activity_service.activity_dict(activity) for activity in activities]
    return activity_models, num, err


def find_activity(id):
    (activity, err) = activity_service.find_activity(id)
    if err is not None:
        return None, None, err
    if activity is None:
        return None, None, None
    (activity_model, err) = activity_service.activity_dict(activity)
    return activity_model, err


def find_activity_users(id, condition):
    (activity_users, num, err) = activity_service.find_activity_users(id, condition)
    if err is not None:
        return None, None, err
    activity_users_model = list()
    for activity_user in activity_users:
        (activity_user_model, err) = activity_service.activity_user_dict(id, activity_user)
        if err is not None:
            return None, None, err
        activity_users_model.append(activity_user_model)
    return activity_users_model, num, err


def find_activity_user(id, username):
    (activity_user, err) = activity_service.find_activity_user(id, username)
    if err is not None:
        return None, err
    activity_user_model = activity_service.activity_user_dict(id, activity_user)
    return activity_user_model, err


def insert_activity_user(id, request_json):
    (ifSuccess, err) = activity_service.insert_activity_user(id, request_json)
    return ifSuccess, err


def update_activity_user(id, username, request_json):
    (ifSuccess, err) = activity_service.update_activity_user(id, username, request_json)
    return ifSuccess, err


def delete_activity_user(id, username):
    (ifSuccess, err) = activity_service.delete_activity_user(id, username)
    return ifSuccess, err


def find_current_user_activities(username, condition=None):
    (current_user_activities, num, err) = activity_service.find_current_user_activities(username, condition)
    if err is not None:
        return None, None, err
    state = condition['state']
    current_user_activities_model = []
    if state == 'hasAttended':
        current_user_activities_model = [activity_service.has_attended_activity_dict(current_user_activity, username)
                                         for current_user_activity in current_user_activities]
    if state == 'canAttend':
        current_user_activities_model = [activity_service.can_attend_activity_dict(current_user_activity) for
                                         current_user_activity in current_user_activities]
    return current_user_activities_model, num, err

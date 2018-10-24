from app.core.services import activity_service
from app.utils.Error import CustomError


def insert_activity(request_json):
    (ifSuccess, err) = activity_service.insert_activity(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_activity(id, request_json):
    (ifSuccess, err) = activity_service.update_activity(id, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def delete_activity(id):
    (ifSuccess, err) = activity_service.delete_activity(id)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_activities(condition):
    (activities, num, err) = activity_service.find_activities(condition)
    if err is not None:
        return None, None, err
    activity_models = list()
    for activity in activities:
        (activity_model, err) = activity_service.activity_to_dict(activity)
        if err is not None:
            return None, None, err
        activity_models.append(activity_model)
    return activity_models, num, None


def find_activity(id):
    (activity, err) = activity_service.find_activity(id)
    if err is not None:
        return None, None, err
    if activity is None:
        return None, None, None
    (activity_model, err) = activity_service.activity_to_dict(activity)
    if err is not None:
        return None, err
    return activity_model, None


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
    return activity_users_model, num, None


def find_activity_user(id, username):
    (activity_user, err) = activity_service.find_activity_user(id, username)
    if err is not None:
        return None, err
    (activity_user_model, err) = activity_service.activity_user_dict(id, activity_user)
    if err is not None:
        return None, err
    return activity_user_model, None


def insert_activity_user(id, request_json):
    (ifSuccess, err) = activity_service.insert_activity_user(id, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_activity_user(id, username, request_json):
    (ifSuccess, err) = activity_service.update_activity_user(id, username, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def delete_activity_user(id, username):
    (ifSuccess, err) = activity_service.delete_activity_user(id, username)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_current_user_activities(username, condition=None):
    (current_user_activities, num, err) = activity_service.find_current_user_activities(username, condition)
    if err is not None:
        return None, None, err
    state = condition['state'] if 'state' in condition else None
    if state is None:
        return None, None, CustomError(500, 200, 'state must be given')
    state_list = ['hasAttended', 'canAttend']
    if state not in state_list:
        return None, None, CustomError(500, 200, 'state error')
    current_user_activities_model = []
    if state == 'hasAttended':
        for current_user_activity in current_user_activities:
            (current_user_activity_model, err) = activity_service.has_attended_activity_dict(current_user_activity,
                                                                                             username)
            if err is not None:
                return None, None, err
            current_user_activities_model.append(current_user_activity_model)
    if state == 'canAttend':
        for current_user_activity in current_user_activities:
            (current_user_activity_model, err) = activity_service.can_attend_activity_dict(current_user_activity)
            if err is not None:
                return None, None, err
            current_user_activities_model.append(current_user_activities_model)
    return current_user_activities_model, num, None

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
    return activities, num, err


def find_activity(id):
    (activity, err) = activity_service.find_activity(id)
    return activity, err


def find_activity_users(id, condition):
    (activity_users, num, err) = activity_service.find_activity_users(id, condition)
    return activity_users, num, err


def find_activity_user(id, username):
    (activity_user, err) = activity_service.find_activity_user(id, username)
    return activity_user, err


def insert_activity_user(id, request_json):
    (ifSuccess, err) = activity_service.insert_activity_user(id, request_json)
    return ifSuccess, err


def update_activity_user(id, username, request_json):
    (ifSuccess, err) = activity_service.update_activity_user(id, username, request_json)
    return ifSuccess, err


def delete_activity_user(id, username):
    (ifSuccess, err) = activity_service.delete_activity_user(id, username)
    return ifSuccess, err


def find_current_user_activities(condition=None):
    (current_user_activities, num,  err) = activity_service.find_current_user_activities(condition)
    return current_user_activities, num, err

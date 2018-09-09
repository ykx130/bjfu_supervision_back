from app.core.services import user_service, supervisor_service


def find_users(condition):
    (users, num, err) = user_service.find_users(condition)
    return users, num, err


def has_user(username):
    (ifSuccess, err) = user_service.has_user(username)
    return ifSuccess, err


def user_to_dict(user):
    return user_service.user_to_dict(user)


def find_user(username):
    (user, err) = user_service.find_user(username)
    return user, err


def insert_user(request_json):
    (ifSuccess, err) = user_service.insert_user(request_json)
    return ifSuccess, err


def delete_user_roles(username, term):
    (ifSuccess, err) = user_service.delete_user_roles(username, term)
    return ifSuccess, err


def update_user(username, request_json):
    (ifSuccess, err) = user_service.update_user(username, request_json)
    if err is not None:
        return ifSuccess, err
    (ifSuccess, err) = user_service.update_user_role(username, request_json)
    return ifSuccess, err


def find_supervisors(condition):
    (supervisors, num, err) = supervisor_service.get_supervisors(condition)
    return supervisors, num, err


def find_supervisors_expire(condition):
    (supervisors, num, err) = supervisor_service.get_supervisors_expire(condition)
    return supervisors, num, err


def batch_renewal(request_json):
    (ifSuccess, err) = user_service.batch_renewal(request_json)
    return ifSuccess, err


def delete_user(username):
    (ifSuccess, err) = user_service.delete_user(username)
    return ifSuccess, err


def find_role(role_name):
    (role, err) = user_service.find_users(role_name)
    return role, err


def find_roles(condition):
    (roles, num, err) = user_service.find_roles(condition)
    return roles, num, err


def insert_role(request_json):
    (ifSuccess, err) = user_service.insert_role(request_json)
    return ifSuccess, err


def update_role(role_name, request_json):
    (ifSuccess, err) = user_service.update_role(role_name, request_json)
    return ifSuccess, err


def delete_role(role_name):
    (ifSuccess, err) = user_service.delete_role(role_name)
    return ifSuccess, err


def find_groups(condition):
    (groups, num, err) = user_service.find_groups(condition)
    return groups, num, err

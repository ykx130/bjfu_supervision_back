from app.core.services import user_service, supervisor_service


def find_users(condition):
    (users, num, err) = user_service.find_users(condition)
    if err is not None:
        return None, None, err
    users_model = list()
    for user in users:
        (user_model, err) = user_service.user_to_dict(user)
        if err is not None:
            return None, 0, err
        users_model.append(user_model)
    return users_model, num, err


def has_user(username):
    (ifSuccess, err) = user_service.has_user(username)
    return ifSuccess, err


def user_to_dict(user):
    (user_model, err) = user_service.user_to_dict(user)
    return user_model, err


def find_user(username):
    (user, err) = user_service.find_user(username)
    if err is not None:
        return None, err
    if user is None:
        return None, None
    (user_model, err) = user_service.user_to_dict(user)
    return user_model, err


def insert_user(request_json):
    (ifSuccess, err) = user_service.insert_user(request_json)
    return ifSuccess, err


def delete_user_roles(username, term):
    (ifSuccess, err) = user_service.delete_user_roles(username, term)
    return ifSuccess, err


def update_user(username, request_json):
    (ifSuccess, err) = user_service.update_user(username, request_json)
    return ifSuccess, err


def find_supervisors(condition):
    (supervisors, num, err) = supervisor_service.get_supervisors(condition)
    supervisors_model = list()
    for supervisor in supervisors:
        (user, err) = user_service.find_user(supervisor.username)
        if err is not None:
            return None, None, err
        (supervisor_model, err) = supervisor_service.supervisor_to_dict(user, supervisor)
        if err is not None:
            return None, None, err
        supervisors_model.append(supervisor_model)
    return supervisors_model, num, err


def find_supervisors_expire(condition):
    (supervisors, num, err) = supervisor_service.get_supervisors_expire(condition)
    supervisors_model = list()
    for supervisor in supervisors:
        (supervisor_model, err) = user_service.user_to_dict(supervisor)
        if err is not None:
            return None, None, err
        supervisors_model.append(supervisor_model)
    return supervisors_model, num, err


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
    roles_model = list()
    for role in roles:
        (role_model, err) = user_service.role_to_dict(role)
        if err is not None:
            return None, None, err
        roles_model.append(role_model)
    return roles_model, num, err


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

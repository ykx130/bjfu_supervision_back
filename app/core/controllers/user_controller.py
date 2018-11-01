from app.core.services import user_service, supervisor_service, lesson_record_service
from app.streaming import send_kafka_message


def find_users(condition):
    (users, num, err) = user_service.find_users(condition)
    if err is not None:
        return None, None, err
    users_model = list()
    for user in users:
        (user_model, err) = user_service.user_to_dict(user)
        if err is not None:
            return None, None, err
        users_model.append(user_model)
    return users_model, num, None


def has_user(username):
    (ifSuccess, err) = user_service.has_user(username)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_user(username):
    (user, err) = user_service.find_user(username)
    if err is not None:
        return None, err
    (user_model, err) = user_service.user_to_dict(user)
    if err is not None:
        return None, err
    return user_model, None


def insert_user(request_json):
    (ifSuccess, err) = user_service.insert_user(request_json)
    if err is not None:
        return None, err
    role_names = request_json.get('role_names', [])
    if '督导' in role_names:
        send_kafka_message(topic='user_service',
                           method='add_supervisor',
                           usernames=[request_json.get('username', None)])
    return ifSuccess, None


def delete_user_roles(username, term):
    (ifSuccess, err) = user_service.delete_user_roles(username, term)
    if err is not None:
        return None, err
    return ifSuccess, None


def update_user(username, request_json):
    (ifSuccess, err) = user_service.update_user(username, request_json)
    if err is not None:
        return None, err
    role_names = request_json.get('role_names', [])
    if '督导' in role_names:
        send_kafka_message(topic='user_service',
                           method='add_supervisor',
                           usernames=[username])
    return ifSuccess, None


def find_supervisors(condition):
    (supervisors, num, err) = supervisor_service.get_supervisors(condition)
    if err is not None:
        return None, None, err
    supervisors_model = list()
    for supervisor in supervisors:
        (user, err) = user_service.find_user(supervisor.username)
        if err is not None:
            return None, None, err
        (supervisor_model, err) = supervisor_service.supervisor_to_dict(user, supervisor)
        if err is not None:
            return None, None, err
        supervisors_model.append(supervisor_model)
    return supervisors_model, num, None


def find_supervisors_expire(condition):
    (supervisors, num, err) = supervisor_service.get_supervisors_expire(condition)
    if err is not None:
        return None, None, err
    supervisors_model = list()
    for supervisor in supervisors:
        (supervisor_model, err) = user_service.user_to_dict(supervisor)
        if err is not None:
            return None, None, err
        supervisors_model.append(supervisor_model)
    return supervisors_model, num, None


def batch_renewal(request_json):
    (ifSuccess, err) = user_service.batch_renewal(request_json)
    if err is not None:
        return False, err
    send_kafka_message(topic='user_service',
                       method='add_supervisor',
                       usernames=[request_json.get('usernames', None)])
    return ifSuccess, None


def delete_user(username):
    (ifSuccess, err) = user_service.delete_user(username)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_role(role_name):
    (role, err) = user_service.find_users(role_name)
    if err is not None:
        return None, err
    return role, None


def find_roles(condition):
    (roles, num, err) = user_service.find_roles(condition)
    if err is not None:
        return None, None, err
    roles_model = list()
    for role in roles:
        (role_model, err) = user_service.role_to_dict(role)
        if err is not None:
            return None, None, err
        roles_model.append(role_model)
    return roles_model, num, None


def insert_role(request_json):
    (ifSuccess, err) = user_service.insert_role(request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def update_role(role_name, request_json):
    (ifSuccess, err) = user_service.update_role(role_name, request_json)
    if err is not None:
        return False, err
    return ifSuccess, None


def delete_role(role_name):
    (ifSuccess, err) = user_service.delete_role(role_name)
    if err is not None:
        return False, err
    return ifSuccess, None


def find_groups(condition):
    (groups, num, err) = user_service.find_groups(condition)
    if err is not None:
        return None, None, err
    groups_model = list()
    for group in groups:
        (group_model, err) = user_service.group_to_dict(group)
        if err is not None:
            return None, None, err
        groups_model.append(group_model)
    return groups_model, num, None

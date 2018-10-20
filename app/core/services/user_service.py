from sqlalchemy.sql import and_
from app.utils.mysql import db
from app.core.models.user import UserRole, User, Role, Group, Supervisor
from app.core.models.lesson import Term, SchoolTerm
from app.utils.misc import convert_datetime_to_string
from flask_login import current_user


def find_users(condition):
    try:
        users = User.users(condition)
    except Exception as e:
        return None, None, e
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def has_user(username):
    try:
        user = User.query.filter(User.username == username).filter(User.using == True).first()
    except Exception as e:
        return False, e
    return False, None if user is None else True, None


def user_to_dict(user):
    try:
        user_dict = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'sex': user.sex,
            'email': user.email,
            'phone': user.phone,
            'state': user.state,
            'unit': user.unit,
            'status': user.status,
            'work_state': user.work_state,
            'prorank': user.prorank,
            'skill': user.skill,
            'group': user.group,
            'role_names': [role.name for role in user.roles]
        }
    except Exception as e:
        return None, e
    return user_dict, None


def find_user(username):
    try:
        user = User.query.filter(User.username == username).filter(User.using == True).first()
    except Exception as e:
        return None, e
    return user, None


def insert_user(request_json):
    user = User()
    username = request_json['username'] if 'username' in request_json else None
    if username is None:
        return False, None
    for key, value in request_json.items():
        if key == 'password':
            user.password = value
        if hasattr(user, key):
            setattr(user, key, value)
    db.session.add(user)
    term = request_json['term'] if 'term' in request_json else Term.query.order_by(Term.name.desc()).filter(
        Term.using == True).first().name
    role_names = request_json['role_names'] if 'role_names' in request_json else []
    for role_name in role_names:
        if role_name == "督导":
            insert_supervisor(term, username)
        user_role = UserRole()
        role = Role.query.filter(Role.name == role_name).filter(Term.using == True).first()
        user_role.username = user.username
        user_role.role_id = role.id
        user_role.term = term
        db.session.add(user_role)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def insert_supervisor(term, username):
    school_term = SchoolTerm(term)
    for i in range(0, 4):
        supervisor = Supervisor()
        supervisor.term = school_term.term_name
        supervisor.username = username
        school_term = school_term + 1
        db.session.add(supervisor)


def delete_user_roles(username, term):
    user_roles = UserRole.filter(UserRole.term == term).filter(UserRole.username == username).filter(
        UserRole.using == True)
    for user_role in user_roles:
        user_role.using = False
        db.session.add(user_role)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def update_user(username, request_json):
    if username is None:
        return False, None
    user = User.query.filter(User.username == username).filter(UserRole.using == True).first()
    if user is None:
        return False, 'User not found'
    for key, value in request_json.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.session.add(user)
    role_names = request_json["role_names"] if "role_names" in request_json else []
    term = request_json['term'] if request_json is not None and 'term' in request_json else Term.query.order_by(
        Term.name.desc()).filter(Term.using == True).first().name
    old_role_names = [role.name for role in user.roles]
    new_role_names = list(set(old_role_names) - set(role_names))
    del_role_names = list(set(role_names) - set(old_role_names))
    if "督导" in del_role_names:
        del_role_names.remove("督导")
        delete_supervisor(term, username)
    if "督导" in new_role_names:
        new_role_names.remove("督导")
        insert_supervisor(term, username)
    del_roles = UserRole.query.filter(UserRole.term == term).filter(UserRole.username == username).filter(
        UserRole.role_name.in_(del_role_names)).filter(UserRole.using == True)
    for del_role in del_roles:
        del_role.using = True
        db.session.add(del_role)
    for new_role_name in new_role_names:
        user_role = UserRole()
        user_role.username = username
        user_role.role_name = new_role_name
        user_role.term = term
        db.session.add(user_role)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def batch_renewal(request_json=None):
    usernames = request_json['usernames'] if 'usernames' in request_json else None
    term = request_json['term'] if 'term' in request_json else Term.query.order_by(Term.name.desc()).filter(
        Term.using == True).first().name
    if usernames is None:
        return False, None
    school_term = SchoolTerm(term)
    for username in usernames:
        for i in range(4):
            new_term = school_term + 1
            user_role = UserRole()
            user_role.username = username
            user_role.role_name = "督导"
            user_role.term = new_term.term_name
            db.session.add(user_role)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def delete_supervisor(term, username):
    supervisors = Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.term >= term).filter(
        Supervisor.using == True)
    for supervisor in supervisors:
        supervisor.using = False
        db.session.add(supervisor)


def delete_user(username):
    try:
        user = User.query.filter(User.username == username).filter(User.using == True).first()
    except Exception as e:
        return False, e
    if user is None:
        return False, None
    user.using = False
    db.session.add(user)
    for user_role in UserRole.query.filter(UserRole.username == username).filter(UserRole.using == True):
        user_role.using = False
        db.session.add(user_role)
    for supervisor_user in Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.using == True):
        supervisor_user.using = False
        db.session.add(supervisor_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def find_role(role_name):
    try:
        role = Role.query.filter(Role.name == role_name).filter(Role.using == True).first()
    except Exception as e:
        return None, e
    if role is None:
        return None, None
    return role, None


def find_roles(condition):
    try:
        roles = Role.roles(condition)
    except Exception as e:
        return None, None, e
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = roles.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, None


def insert_role(request_json):
    role = Role()
    for key, value in request_json:
        if hasattr(role, key):
            setattr(role, key, value)
    db.session.add(role)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def update_role(role_name, request_json):
    try:
        role = Role.query.filter(Role.name == role_name).filter(Role.using == True).first()
    except Exception as e:
        return False, e
    for key, value in request_json:
        if hasattr(role, key):
            setattr(role, key, value)
    try:
        db.session.add(role)
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def delete_role(role_name):
    try:
        role = Role.query.filter(Role.name == role_name).filter(Role.using == True)
    except Exception as e:
        return False, e
    if role is None:
        return None, None
    role.using = True
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def find_groups(condition):
    try:
        groups = Group.groups(condition)
    except Exception as e:
        return None, None, e
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = groups.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, None

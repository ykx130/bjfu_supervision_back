from app import db
from app.core.models.user import UserRole, User, Role, Group
from app.core.models.lesson import Term
from app.utils.misc import convert_datetime_to_string

def find_users(condition):
    users = User.users(condition)
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total


def has_user(username):
    user = User.query.filter(User.username == username).first()
    return False if user is None else True


def user_to_json(user):
    return {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'start_time': convert_datetime_to_string(user.start_time),
            'end_time': convert_datetime_to_string(user.end_time),
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

def find_user(username):
    return User.query.filter(User.username == username).first()


def insert_user(request_json):
    user = User()
    for key, value in request_json.items():
        if key == 'password':
            user.password = value
        if hasattr(user, key):
            setattr(user, key, value)
    db.session.add(user)
    db.session.commit()
    term = Term.query.order_by(Term.id.desc()).first().name
    role_names = request_json['role_names'] if 'role_names' not in request_json else []
    for role_name in role_names:
        user_role = UserRole()
        role = Role.query.filter(Role.name == role_name).first()
        user_role.user_id = user.id
        user_role.role_id = role.id
        user_role.term = term
        db.session.add(user_role)
    db.session.commit()


def update_user(username, request_json):
    if username is None:
        return None
    user = User.query.filter(User.username==username).first()
    for key, value in request_json.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.session.add(user)
    db.session.commit()
    term = Term.query.order_by(Term.id.desc()).first().name
    if 'role_names' in request_json:
        [db.session.delete(user_role) for user_role in UserRole.query.filter(UserRole.user_id == user.id).filter(UserRole.term == term)]
        for role_name in request_json['role_names']:
            user_role = UserRole()
            role = Role.query.filter(Role.name == role_name).first()
            user_role.role_id = role.id
            user_role.user_id = user.id
            user_role.term = term
            db.session.add(user_role)
        db.session.commit()
    return None


def delete_user(username):
    user = User.query.filter(User.username == username).first()
    db.session.delete(user)
    db.session.commit()


def find_role(role_name):
    return Role.query.filter(Role.name == role_name).first()


def find_roles(condition):
    roles = Role.roles(condition)
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = roles.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total



def insert_role(request_json):
    role = Role()
    for key, value in request_json:
        if hasattr(role, key):
            setattr(role, key, value)
    db.session.add(role)
    db.session.commit()


def update_role(role_name,request_json):
    role = Role.query.filter(Role.name == role_name).first()
    for key, value in request_json:
        if hasattr(role, key):
            setattr(role, key, value)
    db.session.add(role)
    db.session.commit()


def delete_role(role_name):
    role = Role.query.filter(Role.name == role_name)
    db.session.delete(role)
    db.session.commit()


def find_groups(condition):
    groups = Group.groups(condition)
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = groups.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total
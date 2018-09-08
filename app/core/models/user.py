from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime
from flask import jsonify
from functools import wraps


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), index=True, default="")
    name = db.Column(db.String(64), default="")
    password_hash = db.Column(db.String(128), default="")
    sex = db.Column(db.String(16), default="男")
    email = db.Column(db.String(64), default="")
    phone = db.Column(db.String(16), default="")
    state = db.Column(db.String(8), default="")
    unit = db.Column(db.String(8), default="")
    status = db.Column(db.String(8), default="")
    work_state = db.Column(db.String(8), default="")
    prorank = db.Column(db.String(8), default="")
    skill = db.Column(db.String(16), default="")
    group = db.Column(db.String(16), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def users(condition: dict):
        name_map = {'users': User, 'roles': Role, 'groups': Group, 'user_roles': UserRole}
        users = User.query.outerjoin(UserRole, UserRole.username == User.username).outerjoin(Role,
                                                                                             UserRole.role_id == Role.id).filter(
            User.using == True)
        for key, value in condition.items():
            if hasattr(User, key):
                users = users.filter(getattr(User, key) == value)
            elif '.' in key:
                items = key.split('.')
                table = name_map[items[0]]
                users = users.filter(getattr(table, items[1]) == value)
        return users

    @property
    def roles(self):
        return Role.query.join(UserRole, UserRole.role_id == Role.id).filter(UserRole.username == self.username).filter(
            Role.using == True).filter(UserRole.using == True).filter(User.using == True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property
    def permissions(self):
        permissions = list()
        for role in self.roles:
            permissions = permissions.extend(role.permissions)
        permissions = set(permissions)
        return permissions

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def can(self, perm: str):
        return perm in self.permissions


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False


login_manager.anonymous_user = AnonymousUser


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), unique=True, default="")
    leader_name = db.Column(db.String(64), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def groups(condition):
        groups = Group.query.filter(Group.using == True)
        for key, value in condition.items():
            if hasattr(Group, key):
                groups = groups.filter(getattr(Group, key) == value)
        return groups

    @property
    def leader(self):
        return User.query.join(Group, User.username == Group.leader_name).filter(Group.id == self.id).filter(
            Group.using == True).first()


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default="")
    role_name = db.Column(db.string(32), default="")
    term = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def user_roles(condition):
        return UserRole.query.filter(UserRole.using == True)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), unique=True, default="")
    permissions = db.Column(db.JSON, default=[])
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def roles(condition):
        roles = Role.query.filter(Role.using == True)
        for key, value in condition.items():
            if hasattr(Role, key):
                roles = roles.filter(getattr(Role, key) == value)
        return roles


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(255), default="")
    username = db.Column(db.String(64), default="")
    detail = db.Column(db.String(1023), default="")
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now())
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def events(condition):
        event_data = Event.query.filter(Event.using == True)
        for key, value in condition.items():
            if hasattr(Event, key):
                event_data = event_data.filter(getattr(Event, key) == value)
        return event_data


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                return jsonify(status="fail", data=[], reason="no permission")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

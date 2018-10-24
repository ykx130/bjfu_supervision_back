from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.mysql import db
from app import login_manager
from datetime import datetime
from flask import jsonify
from functools import wraps
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query


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
    prorank = db.Column(db.String(8), default="")
    skill = db.Column(db.String(16), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def users(condition: dict):
        name_map = {'users': User, 'roles': Role, 'groups': Group, 'user_roles': UserRole, 'supervisors': Supervisor}
        query = User.query.outerjoin(UserRole, UserRole.username == User.username).outerjoin(Supervisor,
                                                                                             Supervisor.username == User.username).outerjoin(
            Role, UserRole.role_name == Role.name).filter(User.using == True)
        url_condition = UrlCondition(condition)
        query = process_query(query, url_condition, name_map, User)
        return query

    @property
    def roles(self, term=None):
        from app.core.models.lesson import Term
        term = term if term is not None else Term.query.order_by(Term.name.desc()).filter(
            Term.using == True).first().name
        role_names = [user_role.role_name for user_role in
                      UserRole.query.filter(UserRole.username == self.username).filter(UserRole.using == True).filter(
                          UserRole.term == term)]
        supervisor = Supervisor.query.filter(Supervisor.term == term).filter(
            Supervisor.username == self.username).filter(Supervisor.using == True).first()
        if supervisor is not None:
            role_names.append("督导")
        return Role.query.filter(Role.name.in_(role_names)).filter(Role.using == True)

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
        name_map = {'groups': Group}
        url_condition = UrlCondition(condition)
        query = Group.query.filter(Group.using == True)
        query = process_query(query, url_condition, name_map, Group)
        return query

    @property
    def leader(self):
        return User.query.join(Group, User.username == Group.leader_name).filter(Group.id == self.id).filter(
            Group.using == True).first()


class Supervisor(db.Model):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default="")
    group = db.Column(db.String(16), default="")
    work_state = db.Column(db.String(8), default="")
    term = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def supervisors(condition):
        name_map = {"supervisors": Supervisor}
        url_condition = UrlCondition(condition)
        user_query = User.query.filter(User.using == True)
        user_query = process_query(user_query, url_condition, name_map, User)
        supervisors = Supervisor.query.filter(Supervisor.username.in_([user.username for user in user_query])).filter(
            Supervisor.using == True)
        for key, value in condition:
            if hasattr(Supervisor, key):
                supervisors = supervisors.filter(getattr(Supervisor, key) == value)
        return supervisors


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default="")
    role_name = db.Column(db.String(32), default="")
    term = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def user_roles(condition):
        name_map = {"user_roles": UserRole}
        url_condition = UrlCondition(condition)
        query = UserRole.query.filter(UserRole.using == True)
        query = process_query(query, url_condition, name_map, UserRole)
        return query


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), unique=True, default="")
    permissions = db.Column(db.JSON, default=[])
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def roles(condition):
        name_map = {"roles": Role}
        url_condition = UrlCondition(condition)
        query = Role.query.filter(Role.using == True)
        query = process_query(query, url_condition, name_map, Role)
        return query


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(255), default="")
    username = db.Column(db.String(64), default="")
    detail = db.Column(db.String(1023), default="")
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now)
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def events(condition):
        name_map = {"events": Event}
        url_condition = UrlCondition(condition)
        query = Event.query.filter(Event.using == True)
        query = process_query(query, url_condition, name_map, Event)
        return query


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

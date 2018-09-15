from app.core.models.user import User, UserRole, Supervisor
from app.core.models.lesson import Term, SchoolTerm
from app.utils.mysql import db


def get_supervisor(username=None, term=None):
    term = term if term is not None else Term.query.order_by(
        Term.name.desc()).filter(Term.using == True).first().name
    try:
        supervisor = Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.term == term).filter(
            Supervisor.using == True).first()
    except Exception as e:
        return None, e
    if supervisor is None:
        return None, None
    try:
        user = User.filter(User.username).filter(User.using == True).first()
    except Exception as e:
        return None, e
    if user is None:
        return None, None
    return user, None


def get_supervisors(condition=None):
    term = condition['term'] if condition is not None and 'term' in condition else Term.query.order_by(
        Term.name.desc()).filter(Term.using == True).first().name
    supervisors = Supervisor.query.filter(Supervisor.term == term).filter(Supervisor.using == True)
    users = User.query.filter(User.username.in_([supervisor.username for supervisor in supervisors])).filter(
        User.using == True)
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def get_supervisors_expire(condition=None):
    term = condition['term'] if condition is not None and 'term' in condition else Term.query.order_by(
        Term.name.desc()).filter(Term.using == True).first().name
    new_term = (SchoolTerm(term) + 1).term_name
    all_usernames = [supervisor.username for supervisor in
                     Supervisor.query.filter(Supervisor.term == term).filter(Supervisor.using == True)]
    can_usernames = [supervisor.username for supervisor in
                     Supervisor.query.filter(Supervisor.term == new_term).filter(Supervisor.using == True)]
    expire_usernames = list(set(all_usernames) - set(can_usernames))
    try:
        users = User.query.filter(User.username.in_(expire_usernames))
        for key, value in condition.items():
            if hasattr(User, key):
                users = users.filter(getattr(User, key) == value)
    except Exception as e:
        return None, None, e
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None

from app.core.models.user import User, Supervisor
from app.core.models.lesson import Term, SchoolTerm
from app.utils.mysql import db
from app.utils.Error import CustomError


def get_supervisor(username=None, term=None):
    try:
        term = term if term is not None else Term.query.order_by(
            Term.name.desc()).filter(Term.using == True).first().name
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    try:
        supervisor = Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.term == term).filter(
            Supervisor.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if supervisor is None:
        return None, CustomError(404, 404, 'supervisor not found')
    try:
        user = User.filter(User.username).filter(User.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if user is None:
        return None, CustomError(404, 404, 'user not found')
    return user, None


def get_supervisors(condition=None):
    try:
        term = condition['term'] if condition is not None and 'term' in condition else Term.query.order_by(
            Term.name.desc()).filter(Term.using == True).first().name
        supervisors = Supervisor.query.filter(Supervisor.term == term).filter(Supervisor.using == True)
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    page = int(condition['_page'][0]) if '_page' in condition else 1
    per_page = int(condition['_per_page'][0]) if '_per_page' in condition else 20
    pagination = supervisors.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def get_supervisors_expire(condition=None):
    try:
        term = condition['term'] if condition is not None and 'term' in condition else Term.query.order_by(
            Term.name.desc()).filter(Term.using == True).first().name
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    new_term = (SchoolTerm(term) + 1).term_name
    try:
        all_usernames = [supervisor.username for supervisor in
                         Supervisor.query.filter(Supervisor.term == term).filter(Supervisor.using == True)]
        can_usernames = [supervisor.username for supervisor in
                         Supervisor.query.filter(Supervisor.term == new_term).filter(Supervisor.using == True)]
        expire_usernames = list(set(all_usernames) - set(can_usernames))
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    try:
        users = User.query.filter(User.username.in_(expire_usernames))
        for key, value in condition.items():
            if hasattr(User, key):
                users = users.filter(getattr(User, key) == value)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page'][0]) if '_page' in condition else 1
    per_page = int(condition['_per_page'][0]) if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def insert_supervisor(request_json):
    username = request_json.get('username', None)
    if username is None:
        return False, CustomError(500, 200, 'username must be given')
    user = User.query.filter(User.username == username).filter(User.using == True).first()
    user.guider = True
    db.session.add(user)
    term = request_json.get('term', None)
    if term is None:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    school_term = SchoolTerm(term)
    for i in range(0, 4):
        supervisor = Supervisor()
        supervisor.term = school_term.term_name
        for key, value in request_json.items():
            if key == 'term':
                continue
            if hasattr(supervisor, key):
                setattr(supervisor, key, value)
        school_term = school_term + 1
        db.session.add(supervisor)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def get_supervisor_num(term=None):
    if term is None:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    if term is None:
        return None, CustomError(404, 404, "term not found")
    supervisors = Supervisor.query.filter(Supervisor.term == term).filter(Supervisor.using == True).all()
    return len(supervisors), None

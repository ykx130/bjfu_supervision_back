from sqlalchemy.sql import and_
from app.utils.mysql import db
from app.core.models.user import User, Group, Supervisor
from app.core.models.lesson import Term, SchoolTerm
from app.utils.Error import CustomError
from flask_login import current_user


def find_users(condition):
    try:
        users = User.users(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def has_user(username):
    try:
        user = User.query.filter(User.username == username).filter(User.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    return False, None if user is None else True, None


def group_to_dict(group):
    (leader_model, err) = user_to_dict(group.leader)
    if err is not None:
        return None, err
    try:
        group_dict = {
            'name': group.name,
            'leader': leader_model
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return group_dict, None


def user_role_names(user, term=None):
    if term is None:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    role_list = {'grouper': '小组长', 'main_grouper': '大组长', 'admin': '管理员', 'leader': '领导', 'guider': '督导'}
    role_names = ['教师']
    for role_name_e, role_name_c in role_list.items():
        if hasattr(user, role_name_e) and getattr(user, role_name_e) == True:
            role_names.append(role_name_c)
    if user.guider:
        supervisor = Supervisor.query.filter(Supervisor.username == user.username).filter(
            Supervisor.term == term).filter(Supervisor.using == True).first()
        if supervisor is None:
            return None, CustomError(500, 200, 'user not supervisor')
        for role_name_e, role_name_c in role_list.items():
            if hasattr(supervisor, role_name_e) and getattr(supervisor, role_name_e) == True:
                role_names.append(role_name_c)
    return role_names, None


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
            'prorank': user.prorank,
            'skill': user.skill,
            'guider': user.guider
        }
        term = Term.query.order_by(
            Term.name.desc()).filter(Term.using == True).first().name
        (role_names, err) = user_role_names(user, term)
        if err is not None:
            return None, err
        if user.guider:
            supervisor = Supervisor.query.filter(Supervisor.username == user.username).filter(
                Supervisor.term == term).filter(Supervisor.using == True).first()
            if supervisor is None:
                return None, CustomError(500, 200, 'user not supervisor')
            user_dict['guider'] = {
                'group': supervisor.group,
                'is_grouper': supervisor.grouper,
                'is_main_grouper': supervisor.main_grouper,
                'work_state': supervisor.work_state,
                'term': term,
            }
        user_dict['role_names'] = role_names
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return user_dict, None


def find_user(username):
    try:
        user = User.query.filter(User.username == username).filter(User.using == True).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if user is None:
        return None, CustomError(404, 404, 'user not found')
    return user, None


def insert_user(request_json):
    username = request_json['username'] if 'username' in request_json else None
    if username is None:
        return False, CustomError(500, 200, 'username should be given')
    (ifHave, err) = has_user(username)
    if err is not None:
        return False, err
    if ifHave:
        return False, CustomError(500, 200, 'username has been used')
    user = User()
    for key, value in request_json.items():
        if key == 'password':
            user.password = value
        if hasattr(user, key):
            setattr(user, key, value)
    role_names = request_json['role_names'] if 'role_names' in request_json else []
    role_name_dict = {'教师': 'teacher', '管理员': 'admin', '领导': 'leader'}
    for role_name in role_names:
        role_name_e = role_name_dict[role_name]
        if hasattr(user, role_name_e):
            setattr(user, role_name_e, True)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_supervisor(term, user):
    user.guider = False
    db.session.add(user)
    supervisors = Supervisor.query.filter(Supervisor.username == user.username).filter(Supervisor.term >= term).filter(
        Supervisor.using == True)
    for supervisor in supervisors:
        supervisor.using = False
        db.session.add(supervisor)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def insert_supervisor(user, term, request_json):
    user.guider = True
    db.session.add(user)
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


def update_grouper(term, username, group_name, role_name, add=False):
    group = Group.query.filter(Group.name == group_name).first()
    if group is None:
        return False, CustomError(404, 404, "group does not exist")
    supervisor_terms = Supervisor.query.filter(Supervisor.term >= term).filter(Supervisor.username == username).filter(
        Supervisor.using == True).all()
    if len(supervisor_terms) == 0:
        return False, CustomError(500, 200, 'user must be supervisor')
    for supervisor_term in supervisor_terms:
        setattr(supervisor_term, role_name, add)
        setattr(supervisor_term, 'group', group_name)
        db.session.add(supervisor_term)
    if add:
        group.leader_name = username
    else:
        group.leader_name = ""
    db.session.add(group)
    try:
        db.session.commit()
        db.session.rollback()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_user(username, request_json):
    if username is None:
        return False, CustomError(500, 500, 'username should be given')
    try:
        user = User.query.filter(User.username == username).filter(User.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if user is None:
        return False, CustomError(404, 404, 'user not found')
    for key, value in request_json.items():
        if hasattr(user, key):
            setattr(user, key, value)

    role_names = request_json["role_names"] if "role_names" in request_json else []
    try:
        term = request_json['term'] if request_json is not None and 'term' in request_json else Term.query.order_by(
            Term.name.desc()).filter(Term.using == True).first().name
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    (old_role_names, err) = user_role_names(user, term)
    if err is not None:
        return False, err
    new_role_names = list(set(role_names) - set(old_role_names))
    del_role_names = list(set(old_role_names) - set(role_names))
    if "督导" in del_role_names:
        del_role_names.remove("督导")
        (ifSuccess, err) = delete_supervisor(term, user)
        if err is not None:
            return False, err
    elif "督导" in new_role_names:
        new_role_names.remove("督导")
        (ifSuccess, err) = insert_supervisor(user, term, request_json)
        if err is not None:
            return False, err
    if "小组长" in del_role_names:
        del_role_names.remove("小组长")
        supervisor = Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.using == True).filter(
            Supervisor.term == term).first()
        if supervisor is None:
            return False, 'user must be supervisor'
        group_name = request_json['group_name'] if 'group_name' in request_json else supervisor.group
        (ifSuccess, err) = update_grouper(term, username, group_name, 'grouper', False)
        if err is not None:
            return False, err
    elif "小组长" in new_role_names:
        new_role_names.remove("小组长")
        supervisor_change = Supervisor.query.filter(Supervisor.username == username).filter(
            Supervisor.term == term).filter(Supervisor.using == True).first()
        if supervisor_change is None:
            return False, CustomError(500, 200, "user is not supervisor")
        group_name = request_json['group'] if 'group' in request_json else supervisor_change.group
        grouper = Supervisor.query.filter(Supervisor.term >= term).filter(Supervisor.grouper == True).filter(
            Supervisor.group == group_name).filter(Supervisor.using == True).first()
        if grouper is not None:
            (ifSuccess, err) = update_grouper(term, grouper.username, group_name, '小组长', False)
            if err is not None:
                return False, err
        (ifSuccess, err) = update_grouper(term, username, group_name, 'grouper', True)
        if err is not None:
            return False, err
    if "大组长" in del_role_names:
        del_role_names.remove("大组长")
        (ifSuccess, err) = update_grouper(term, username, 'main_grouper', False)
        if err is not None:
            return False, err
    elif "大组长" in new_role_names:
        new_role_names.remove("大组长")
        grouper = Supervisor.query.filter(Supervisor.term >= term).filter(Supervisor.main_grouper == True).filter(
            Supervisor.using == True).first()
        if grouper is not None:
            (ifSuccess, err) = update_grouper(term, grouper.username, 'main_grouper', False)
            if err is not None:
                return False, err
        (ifSuccess, err) = update_grouper(term, username, "main_grouper", True)
        if err is not None:
            return False, err
    supervisors = Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.term >= term).filter(Supervisor.using == True)
    for supervisor in supervisors:
        for key, value in request_json.items():
            if key == 'term':
                continue
            if hasattr(supervisor, key):
                setattr(supervisor, key, value)
        db.session.add(supervisor)
    role_dict = {'管理员': 'admin', '领导': 'leader'}
    for role_name_c in role_names:
        if role_name_c in role_dict:
            role_name_e = role_dict[role_name_c]
            setattr(user, role_name_e, True)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_user(username):
    try:
        term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first().name
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    try:
        user = User.query.filter(User.username == username).filter(User.using == True).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if user is None:
        return False, CustomError(404, 404, 'user not found')
    user.using = False
    db.session.add(user)
    if user.guider:
        supervisors = Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.using == True).filter(
            Supervisor.term >= term)
        for supervisor in supervisors:
            supervisor.using = False
            db.session.add(supervisor)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def batch_renewal(request_json=None):
    usernames = request_json['usernames'] if 'usernames' in request_json else None
    if usernames is None:
        return False, CustomError(500, 500, 'usernames should be given')
    try:
        term = request_json['term'] if 'term' in request_json else Term.query.order_by(Term.name.desc()).filter(
            Term.using == True).first().name
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    school_term = SchoolTerm(term)
    for username in usernames:
        supervisor = Supervisor.query.filter(Supervisor.username == username).filter(Supervisor.term == term).filter(
            Supervisor.using == True).first()
        if supervisor is None:
            return False, CustomError(500, 200, 'user must be supervisor')
        for i in range(4):
            new_term = school_term + 1
            supervisor_new = Supervisor()
            supervisor_new.username = username
            supervisor_new.term = new_term
            supervisor_new.group = supervisor.group
            db.session.add(supervisor)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def find_groups(condition):
    try:
        groups = Group.groups(condition)
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = condition['_page'] if '_page' in condition else 1
    per_page = condition['_per_page'] if '_per_page' in condition else 20
    pagination = groups.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total, None

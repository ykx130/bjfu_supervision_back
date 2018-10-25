from app.core.models.lesson import NoticeLesson, Term, Lesson
from app.utils.mysql import db
from app.utils.Error import CustomError

def insert_notice_lesson(request_json):
    lesson_id = request_json['lesson_id'] if 'lesson_id' in request_json else None
    term = request_json['term'] if request_json is not None and 'term' in request_json else Term.query.order_by(
        Term.name.desc()).filter(Term.using == True).first().name
    assign_group = request_json['assign_group'] if 'assign_group' in request_json else None
    if assign_group is None:
        return False, CustomError(500,200, 'assign group should be given')
    if lesson_id is None:
        return False, CustomError(500,200, 'lesson id should be given')
    try:
        lesson = Lesson.query.filter(Lesson.id == lesson_id).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    lesson.lesson_level = "关注课程"
    db.session.add(lesson)
    notice_lesson_record = NoticeLesson.query.filter(NoticeLesson.lesson_id == lesson_id).filter(
        NoticeLesson.term == term).filter(NoticeLesson.using == True).first()
    if notice_lesson_record is not None:
        return False, CustomError(500,200, "lesson has been noticed")
    notice_lesson = NoticeLesson()
    notice_lesson.term = term
    for key, value in request_json.items():
        if hasattr(notice_lesson, key):
            setattr(notice_lesson, key, value)
    db.session.add(notice_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def insert_notice_lessons(request_json):
    term = request_json['term'] if request_json is not None and 'term' in request_json else Term.query.order_by(
        Term.name.desc()).filter(Term.using == True).first().name
    lesson_ids = request_json['lesson_ids'] if 'lesson_ids' in request_json else None
    if lesson_ids is None:
        return False, CustomError(500,200, 'lesson_ids should be given')
    try:
        lessons = Lesson.query.filter(Lesson.lesson_id.in_(lesson_ids))
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    for lesson in lessons:
        notice_lesson_record = NoticeLesson.query.filter(NoticeLesson.lesson_id == lesson.lesson_id).filter(
            NoticeLesson.term == term).filter(NoticeLesson.using == True).first()
        if notice_lesson_record is not None:
            return False, CustomError(500,200, "lesson has been noticed")
        lesson.lesson_level = "关注课程"
    assign_group = request_json['assign_group'] if 'assign_group' in request_json else None
    if assign_group is None:
        return False, CustomError(500,200, 'assign group should be given')
    for lesson_id in lesson_ids:
        notice_lesson = NoticeLesson()
        notice_lesson.term = term
        notice_lesson.lesson_id = lesson_id
        notice_lesson.assign_group = assign_group
        db.session.add(notice_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_notice_lesson(id):
    notice_lesson = NoticeLesson.query.filter(NoticeLesson.id == id).filter(NoticeLesson.using == True).first()
    if notice_lesson is None:
        return False, CustomError(404,404, 'notice lesson not found')
    notice_lesson.using = False
    try:
        lesson = Lesson.query.filter(Lesson.lesson_id == notice_lesson.lesson_id).first()
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    if lesson is None:
        return False, CustomError(404,404, 'lesson not found')
    lesson.lesson_level = "自助听课"
    db.session.add(lesson)
    db.session.add(notice_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_notice_lessons(request_json):
    notice_lesson_ids = request_json['notice_lesson_ids'] if 'notice_lesson_ids' in request_json else None
    if notice_lesson_ids is None:
        return False, CustomError(500,200, 'notice_lesson_ids should be given')
    notice_lessons = NoticeLesson.query.filter(NoticeLesson.id.in_(notice_lesson_ids)).filter(
        NoticeLesson.using == True)
    try:
        lessons = Lesson.query.filter(
            Lesson.lesson_id.in_([notice_lesson.lesson_id for notice_lesson in notice_lessons]))
    except Exception as e:
        return False, CustomError(500, 500, str(e))
    for lesson in lessons:
        lesson.lesson_level = "关注课程"
    for notice_lesson in notice_lessons:
        notice_lesson.using = False
        db.session.add(notice_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))


def update_notice_lesson(id, request_json):
    notice_lesson = NoticeLesson.query.filter(NoticeLesson.id == id).filter(NoticeLesson.using == True).first()
    if notice_lesson is None:
        return False, CustomError(404,404, 'notice lesson not found')
    for key, value in request_json.items():
        if hasattr(notice_lesson, key):
            setattr(notice_lesson, key, value)
    db.session.add(notice_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def find_notice_lesson(id):
    notice_lesson = NoticeLesson.query.filter(NoticeLesson.id == id).filter(NoticeLesson.using == True).first()
    if notice_lesson is None:
        return False, CustomError(404,404, 'notice lesson not found')
    return notice_lesson, None


def find_notice_lessons(condition):
    notice_lessons = NoticeLesson.notice_lessons(condition)
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = notice_lessons.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def notice_lesson_to_dict(lesson, notice_lesson):
    try:
        notice_lesson_dict = {
            'id': notice_lesson.id if notice_lesson is not None else None,
            'lesson_id': notice_lesson.lesson_id if lesson is not None else None,
            'lesson_attribute': lesson.lesson_attribute if lesson is not None else None,
            'lesson_state': lesson.lesson_state if lesson is not None else None,
            'lesson_level': lesson.lesson_level if lesson is not None else None,
            'lesson_name': lesson.lesson_name,
            'lesson_teacher_id': lesson.lesson_teacher_id,
            'notice_reason': notice_lesson.notice_reason,
            'votes': notice_lesson.votes,
            'assign_group': notice_lesson.assign_group
        }
    except Exception as e:
        return None,  CustomError(500, 500, str(e))
    return notice_lesson_dict, None


def change_notice_lesson_notice(id, vote=True):
    notice_lesson = NoticeLesson.query.filter(NoticeLesson.id == id).filter(NoticeLesson.using == True)
    if notice_lesson is None:
        return False, CustomError(404,404, 'notice lesson not found')
    if vote:
        notice_lesson.votes = notice_lesson.votes + 1
    notice_lesson.notices = notice_lesson.notices + 1
    db.session.add(notice_lesson)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False,  CustomError(500, 500, str(e))
    return True, None

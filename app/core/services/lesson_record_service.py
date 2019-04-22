from app.core.models.lesson import LessonRecord, Term
from app.core.models.user import User, Supervisor
from app.utils.mysql import db
from app.utils.Error import CustomError
from app.core.services import form_service, user_service, lesson_service


def change_user_lesson_record_num(username, term):
    (total_times, has_submitted_times, to_be_submitted_times, err) = form_service.user_forms_num(username, term)
    if err is not None:
        raise err
    (ifSuccess, err) = update_lesson_record(username, term,
                                            {'total_times': total_times, 'has_submitted': has_submitted_times,
                                             'to_be_submitted': to_be_submitted_times})
    if err is not None:
        raise err

from app.core.services import lesson_record_service
from app.streaming import sub_kafka


@sub_kafka('form_service')
def user_form_service_server(message):
    method = message.get('method')
    if not method:
        return
    if method == 'add_form' or method == 'repulse_form':
        lesson_record_service.change_user_lesson_record_num(message.get('args', {}).get('username', None),
                                                            message.get('args', {}).get('term', None))


@sub_kafka('user_service')
def user_service_server(message):
    method = message.get('method')
    if not method:
        return
    if method == 'add_supervisor' or method == 'update_user':
        lesson_record_service.update_lesson_record_service(message.get('args', {}).get('usernames', None))

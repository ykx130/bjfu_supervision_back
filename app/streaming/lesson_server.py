from app.streaming import sub_kafka

@sub_kafka('lesson_service')
def lesson_service_server(message):
    method = message.get('method')
    if not method:
        return
    if method == 'add_notice_lesson' or method == 'delete_notice_lesson':
        # notice_lesson_service.update_page_data()
        # 更新首页
        pass


@sub_kafka('form_service')
def lesson_form_service_server(message):
    method = message.get('method')
    if not method:
        return
    if method == 'add_form' or method == 'repulse_form':
        # 打回 和 提交更新问卷状态
        # update_lesson_notices(message.get('args', {}).get('lesson_id', None))
        pass

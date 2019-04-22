from app.streaming import sub_kafka

@sub_kafka('notice_service')
def notice_service_server(message):
    # push_new_message(message.get('args', {}).get('username'), message.get('args', {}).get('msg'))
    # 提交
    pass

from app.streaming import sub_kafka
import json


@sub_kafka('form_service')
def form_service_receiver(message):
    method = message.get('method')
    if not method:
        return
    if method == 'add_form' or method == 'repulse_form':
        pass
        # 计算分布
        # calculate_map(message.get('args', {}).get('form', {}).get('bind_meta_name'))
        # update_page_data()

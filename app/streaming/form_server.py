import json
from app.streaming import sub_kafka
from app.core.services import FormService, InterfaceService
from multiprocessing import Process, Queue


@sub_kafka('form_service')
def calculate_form_server(method, args):
    """
    接收到问卷打回或者提交后更新首页和分布计算的数据
    :param method:
    :param args:
    :return:
    """
    if not method:
        return
    if method == 'add_form' or method == 'repulse_form':
        # 计算分布
        InterfaceService.update_page_data()
        FormService.calculate_map(args.get('bind_meta_name'))


if __name__ == '__main__':
    processes = [
        Process(target=calculate_form_server),
    ]
    [p.start() for p in processes]
    [p.join() for p in processes]


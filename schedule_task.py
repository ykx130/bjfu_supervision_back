'''
@Author: your name
@Date: 2019-11-21 23:27:08
@LastEditTime: 2019-11-21 23:57:10
@LastEditors: Please set LastEditors
@Description: In User Settings Edi
@FilePath: /bjfu_supervision_back/schedule_task.py
'''
from app.scripts import lesson_fetch, fetch_origin_lesson, mongodb_back
import schedule
import time

def job_refresh_lesson():
    print("RUN TASK")
    origin_info = {'host':'202.204.121.76', 'user': 'bjlydx_pj', 'passwd': 'bjlydx_pj', 'db': 'orcl',
     'year': '2019-2020', 'semester': '1'} 
    fetch_origin_lesson.update_database(info=origin_info)

    lesson_info = {'term': '2019-2020-1', 'host': 'localhost', 'user': 'rot', 'passwd': 'Root!!2018', 'db': 'supervision',
            'charset': 'utf8'}
    lesson_fetch.update_database(info=lesson_info)

schedule.every().day.at("22:00").do(job_refresh_lesson)
schedule.every(5).hours.do(mongodb_back.run_back)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
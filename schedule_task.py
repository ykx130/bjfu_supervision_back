'''
@Author: your name
@Date: 2019-11-21 23:27:08
@LastEditTime: 2019-11-26 22:31:53
@LastEditors: Please set LastEditors
@Description: In User Settings Edi
@FilePath: /bjfu_supervision_back/schedule_task.py
'''
from app.scripts import lesson_fetch, fetch_origin_lesson, mongodb_back, refresh_lesson_record, refresh_model_lesson_vote
import schedule
import time

def job_refresh_lesson():
    print("RUN TASK")
    origin_info = {'host':'202.204.121.76', 'user': 'bjlydx_pj', 'passwd': 'bjlydx_pj', 'db': 'orcl',
     'year': '2020-2021', 'semester': '1'}
    fetch_origin_lesson.update_database(info=origin_info)

    lesson_info = {'term': '2020-2021-1', 'host': 'localhost', 'user': 'root', 'passwd': 'Root!!2018', 'db': 'supervision',
            'charset': 'utf8'}
    lesson_fetch.update_database(info=lesson_info)

schedule.every().day.at("23:35").do(job_refresh_lesson)
schedule.every(5).hours.do(mongodb_back.run_back)
schedule.every().day.at("09:00").do(refresh_lesson_record.inser_lesson_record)
schedule.every().day.at("12:00").do(refresh_lesson_record.inser_lesson_record)
schedule.every().day.at("14:00").do(refresh_lesson_record.inser_lesson_record)
schedule.every().day.at("17:00").do(refresh_lesson_record.inser_lesson_record)
schedule.every().day.at("19:00").do(refresh_lesson_record.inser_lesson_record)
schedule.every(2).hours.do(refresh_model_lesson_vote.run)



if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
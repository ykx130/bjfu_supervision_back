'''
@Author: your name
@Date: 2019-11-21 10:37:52
@LastEditTime: 2019-11-21 23:56:25
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /bjfu_supervision_back/app/scripts/mongodb_back.py
'''
import os
import datetime
import time
import schedule
from app.utils.misc import convert_datetime_to_string
DB_NAME = 'supervision'
DB_USER = 'superversion'
DB_PASSWD = 'bjfupj2018'
DB_HOST = 'localhost:27017'
PATH_DUMP='mongoexport'  
BACK_DB_FILE = '/var/mongo/backup/{}_{}.json'
COLLECTIONS =  ['form', 'form_meta']


def run_back():
    for c in COLLECTIONS:
        cmd = "mongoexport -h {} -u {} -p {} -d {}  -o {} -c {}".format( DB_HOST, DB_USER, DB_PASSWD,DB_NAME, BACK_DB_FILE.format(c, convert_datetime_to_string(datetime.datetime.now(), "%Y-%m-%d-%H-%M")),c)
        print(cmd)
        print(os.system(cmd))
   
if __name__ == "__main__":
    run_back()
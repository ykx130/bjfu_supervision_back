#!/usr/bin/env python
# -_- coding: utf-8 -_-

import time
from datetime import datetime, timedelta


def convert_datetime_to_timestamp(datetime):
    return int(time.mktime(datetime.timetuple()))


def get_today_string():
    return time.strftime('%Y-%m-%d', time.localtime())


def convert_timestamp_to_string(timestamp, format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format, time.localtime(int(timestamp)))


def convert_struct_time_to_string(struct_time, format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format, struct_time) if struct_time else ''


def convert_datetime_to_string(datetime_time,format="%Y-%m-%d %H:%M:%S"):
    return datetime_time.strftime(format) if datetime_time else ''


def convert_utc_to_ctt(time_str, format="%Y-%m-%d %H:%M:%S"):
    """
    把utc时间转成东8时间
    :param from_str:
    :param to_str:
    :return:
    """
    o_time = datetime.strptime(time_str, format)
    o_time = o_time + timedelta(hours=8)
    return convert_datetime_to_string(o_time, format)


def convert_ctt_to_utc(time_str, format="%Y-%m-%d %H:%M:%S"):
    """
    把东8转utc时间
    :param from_str:
    :param to_str:
    :return:
    """
    o_time = datetime.strptime(time_str, format)
    o_time = o_time - timedelta(hours=8)
    return convert_datetime_to_string(o_time, format)
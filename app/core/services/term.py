'''
@Author: your name
@Date: 2019-11-22 11:42:34
@LastEditTime: 2019-11-22 11:43:04
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /bjfu_supervision_back/app/core/services/term.py
'''
from datetime import datetime
import app.core.dao as dao
from app import cache
from app.utils.Error import CustomError


class TermService(object):
    @classmethod
    @cache.cached(timeout=1000000000)
    def get_now_term(cls):
        date = datetime.now()
        (terms, num) = dao.Term.query_terms(query_dict={'begin_time_lte': [str(date)], 'end_time_gte': [str(date)]})
        if num == 0:
            raise CustomError(500, 200, 'term not exist')
        return terms[0]
    
    @classmethod
    def get_now_term_no_cache(cls):
        date = datetime.now()
        (terms, num) = dao.Term.query_terms(query_dict={'begin_time_lte': [str(date)], 'end_time_gte': [str(date)]})
        if num == 0:
            raise CustomError(500, 200, 'term not exist')
        return terms[0]

from app.utils.mysql import db
from sqlalchemy import text
from datetime import datetime
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query, count_query, page_query
from app.utils.Error import CustomError


class ConsultType(db.Model):
    __tablename__ = 'consult_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, consult_type):
        if consult_type is None:
            return None
        try:
            consult_type_dict = {'id': consult_type.id, 'name': consult_type.name}
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return consult_type_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ConsultType.query
        if not unscoped:
            query = query.filter(ConsultType.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ConsultType)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_consult_type(cls, query_dict, unscoped: bool = False):
        consult_type = ConsultType.query
        if not unscoped:
            consult_type = consult_type.filter(ConsultType.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            consult_type = process_query(consult_type, url_condition.filter_dict, url_condition.sort_limit_dict,
                                         ConsultType).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(consult_type)

    @classmethod
    def insert_consult_type(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        consult_type = ConsultType()
        for key, value in data.items():
            if hasattr(consult_type, key):
                setattr(consult_type, key, value)
        db.session.add(consult_type)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_consult_types(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ConsultType.query
        if not unscoped:
            query = query.filter(ConsultType.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ConsultType)
            (consult_types, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(consult_type) for consult_type in consult_types], total

    @classmethod
    def delete_consult_type(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = ConsultType.query.filter(ConsultType.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ConsultType)
            (consult_types, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for consult_type in consult_types:
            consult_type.using = False
            db.session.add(consult_type)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_consult_type(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = ConsultType.query.filter(ConsultType.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ConsultType)
            (consult_types, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for consult_type in consult_types:
            for key, value in data.items():
                if hasattr(consult_type, key):
                    setattr(consult_type, key, value)
            db.session.add(consult_type)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class Consult(db.Model):
    __tablename__ = 'consults'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    type = db.Column(db.String(16), nullable=False, default='')
    submit_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    answer_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, server_default=text('NOW()'))
    term = db.Column(db.String(16), default='')
    state = db.Column(db.String(16), default='')
    meta_description = db.Column(db.String(255), default='')
    phone = db.Column(db.String(24), default='')
    content = db.Column(db.String(255), default=-1)
    requester_username = db.Column(db.String(16), default='')
    responsor_username = db.Column(db.String(16), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, consult):
        if consult is None:
            return None
        try:
            consult_dict = {
                'id': consult.id,
                'type': consult.type,
                'requester_username': consult.requester_username,
                'submit_time': str(consult.submit_time),
                'answer_time': str(consult.answer_time),
                'term': consult.term,
                'state': consult.state,
                'meta_description': consult.meta_description,
                'phone': consult.phone,
                'responsor_username': consult.responsor_username,
                'content': consult.content
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return consult_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Consult.query
        if not unscoped:
            query = query.filter(Consult.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Consult)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_consult(cls, query_dict:dict, unscoped: bool = False):
        consult = Consult.query
        if not unscoped:
            consult = consult.filter(Consult.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            consult = process_query(consult, url_condition.filter_dict, url_condition.sort_limit_dict,
                                     Consult).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(consult)

    @classmethod
    def insert_consult(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        consult = Consult()
        for key, value in data.items():
            if hasattr(consult, key):
                setattr(consult, key, value)
        db.session.add(consult)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_consults(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Consult.query
        if not unscoped:
            query = query.filter(Consult.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Consult)
            (consults, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(consult) for consult in consults], total

    @classmethod
    def delete_consult(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Consult.query.filter(Consult.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Consult)
            (consults, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for consult in consults:
            consult.using = False
            db.session.add(consult)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_consult(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Consult.query.filter(Consult.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Consult)
            (consults, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for consult in consults:
            for key, value in data.items():
                if hasattr(consult, key):
                    setattr(consult, key, value)
            db.session.add(consult)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

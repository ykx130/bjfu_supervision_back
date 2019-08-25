import app.core.dao as dao
from app.utils import CustomError, db
from flask_login import current_user
from datetime import datetime
from app.utils.Error import CustomError
import app.core.services as service



class ConsultTypeController(object):
    @classmethod
    def formatter(cls, consult_type: dict):
        return consult_type

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def reformatter_query(cls, data: dict):
        return data

    @classmethod
    def get_consult_type(cls, query_dict:dict, unscoped: bool = False):
        consult_type = dao.ConsultType.get_consult_type(query_dict=query_dict, unscoped=unscoped)
        if consult_type is None:
            raise CustomError(404, 404, 'consult_type not found')
        return cls.formatter(consult_type)

    @classmethod
    def query_consult_types(cls, query_dict: dict, unscoped: bool = False):
        (consult_types, num) = dao.ConsultType.query_consult_types(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(consult_type) for consult_type in consult_types], num

    @classmethod
    def insert_consult_type(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data=data)
        try:
            dao.ConsultType.insert_consult_type(ctx=False, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_consult_type(cls, ctx: bool = True, id: int = 0, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_update(data)
        consult_type = dao.ConsultType.get_consult_type(query_dict={'id':id}, unscoped=False)
        if consult_type is None:
            raise CustomError(404, 404, 'consult_type not found')
        try:
            dao.ConsultType.update_consult_type(ctx=False, query_dict={'id': [id]}, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_consult_type(cls, ctx: bool = True, id: int = 0):
        consult_type = dao.ConsultType.get_consult_type(query_dict={'id':id}, unscoped=False)
        if consult_type is None:
            raise CustomError(404, 404, 'consult_type not found')
        try:
            dao.ConsultType.delete_consult_type(ctx=False, query_dict={'id': [id]})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True


class ConsultController(object):
    @classmethod
    def formatter(cls, consult: dict):
        return consult

    @classmethod
    def reformatter_insert(cls, data: dict):
        data['term'] = data.get('term', service.TermService.get_now_term()['name'])
        data['state'] = data.get('state', '待协调')
        data['requester_username'] = data.get('requester_username', current_user.username)
        data['submit_time'] = data.get('submit_time', datetime.now())
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        data['state'] = data.get('state', '已协调')
        data['responsor_username'] = data.get('responsor_username', current_user.username)
        data['answer_time'] = data.get('answer_time', datetime.now())
        return data

    @classmethod
    def reformatter_query(cls, data: dict):
        return data

    @classmethod
    def get_consult(cls, query_dict:dict, unscoped: bool = False):
        consult = dao.Consult.get_consult(query_dict=query_dict, unscoped=unscoped)
        if consult is None:
            raise CustomError(404, 404, 'consult not found')
        return cls.formatter(consult)

    @classmethod
    def query_consults(cls, query_dict: dict, unscoped: bool = False):
        (consults, num) = dao.Consult.query_consults(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(consult) for consult in consults], num

    @classmethod
    def insert_consult(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data=data)
        try:
            dao.Consult.insert_consult(ctx=False, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_consult(cls, ctx: bool = True, id: int = 0, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_update(data)
        consult = dao.Consult.get_consult(query_dict={'id':id}, unscoped=False)
        if consult is None:
            raise CustomError(404, 404, 'consult not found')
        try:
            dao.Consult.update_consult(ctx=False, query_dict={'id': [id]}, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_consult(cls, ctx: bool = True, id: int = 0):
        consult = dao.Consult.get_consult(query_dict={'id':id}, unscoped=False)
        if consult is None:
            raise CustomError(404, 404, 'consult not found')
        try:
            dao.Consult.delete_consult(ctx=False, query_dict={'id': [id]})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

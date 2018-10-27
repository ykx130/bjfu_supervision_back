from app.utils.mysql import db
from sqlalchemy import text
from datetime import datetime
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query


class ConsultType(db.Model):
    __tablename__ = 'consult_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def consult_types(condition):
        url_condition = UrlCondition(condition)
        query = ConsultType.query.filter(ConsultType.using == True)
        name_map = {'consult_types': ConsultType}
        query = process_query(query, url_condition, name_map, ConsultType)
        return query


class Consult(db.Model):
    __tablename__ = 'consults'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    type = db.Column(db.String(16), nullable=False, default="")
    requester_username = db.Column(db.String(16), nullable=False, default="")
    submit_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    answer_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, server_default=text('NOW()'))
    term = db.Column(db.String(16), default="")
    state = db.Column(db.String(16), default="")
    meta_description = db.Column(db.String(255), default="")
    phone = db.Column(db.String(24), default="")
    responsor_username = db.Column(db.String(16), default="")
    content = db.Column(db.String(255), default=-1)
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def consults(condition: dict):
        url_condition = UrlCondition(condition)
        query = Consult.query.filter(Consult.using == True)
        name_map = {'consults': Consult}
        query = process_query(query, url_condition, name_map, Consult)
        return query

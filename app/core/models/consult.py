from app.utils.mysql import db
from datetime import datetime


class ConsultType(db.Model):
    __tablename__ = 'consult_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def consult_types(condition: dict):
        consult_type_data = ConsultType.query.filter(ConsultType.using == True)
        for key, value in condition.items():
            if hasattr(ConsultType, key):
                consult_type_data = consult_type_data.filter(getattr(ConsultType, key) == value)
        return consult_type_data


class Consult(db.Model):
    __tablename__ = 'consults'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    type = db.Column(db.String(16), nullable=False, default="")
    requester_username = db.Column(db.String(16), nullable=False, default="")
    submit_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    answer_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    term = db.Column(db.String(16), default="")
    state = db.Column(db.String(16), default="")
    meta_description = db.Column(db.String(255), default="")
    phone = db.Column(db.String(24), default="")
    responsor_username = db.Column(db.String(16), default="")
    content = db.Column(db.String(255), default=-1)
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def consults(condition: dict):
        consult_data = Consult.query.filter(Consult.using == True)
        for key, value in condition.items():
            if hasattr(Consult, key):
                consult_data = consult_data.filter(getattr(Consult, key) == value)
        return consult_data

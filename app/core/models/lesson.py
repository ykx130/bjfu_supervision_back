from flask_login import UserMixin, AnonymousUserMixin,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask import jsonify
from functools import wraps
import json

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.Integer, default=-1)
    lesson_attribute = db.Column(db.String(8), default="")
    lesson_state = db.Column(db.String(8), default="")
    lesson_level = db.Column(db.String(8), default="")
    lesson_name = db.Column(db.String(32), default="")
    lesson_teacher_id = db.Column(db.String(16), default="")
    lesson_teacher_letter = db.Column(db.String(32), default="")
    lesson_teacher_name = db.Column(db.String(8), default="")
    lesson_teacher_unit = db.Column(db.String(16), default="")
    lesson_unit = db.Column(db.String(16), default="")
    lesson_year = db.Column(db.String(32), default="")
    lesson_semester = db.Column(db.Integer, default="")
    lesson_week = db.Column(db.String(48), default="")
    lesson_time = db.Column(db.String(16), default="")
    lesson_room = db.Column(db.String(16), default="")
    lesson_class = db.Column(db.String(24), default="")
    lesson_type = db.Column(db.String(8), default="")
    lesson_weekday = db.Column(db.Integer, default=0)
    lesson_grade = db.Column(db.String(64), default="")
    assgin_group = db.Column(db.String(8), default="")
    lesson_attention_reason = db.Column(db.String(255), default="")
    lesson_model = db.Column(db.Boolean, default=False)

    @staticmethod
    def lessons(condition):
        lesson_data = Lesson.query
        for key, value in condition.items():
            if hasattr(Lesson, key):
                lesson_data = lesson_data.filter(getattr(Lesson, key)== value)


class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(16))
    begin_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)

    @staticmethod
    def terms(condition):
        terms_data = Term.query
        for key, value in condition:
            if hasattr(Term, key):
                terms_data = terms_data.filter(getattr(Term, key) == value)
        if 'time' in condition:
            terms_data = terms_data.filter(Term.begin_time<condition['time']).filter(Term.end_time>=condition['time'])
        return terms_data




class LessonCase(object):
    def __init__(self):
        self.model = {
            'id':None,
            'lesson_week':None,
            'lesson_time':None,
            'lesson_class': None,
            'lesson_weekday':None,
            'lesson_room':None,
            'assign_group':None,
            'lesson_attention_reason':None
        }

    @property
    def id(self):
        return self.model['id']

    @id.setter
    def id(self, id_data):
        self.model['id'] = id_data

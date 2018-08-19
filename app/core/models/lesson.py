from flask_login import UserMixin, AnonymousUserMixin,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask import jsonify
from functools import wraps
import json

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.Integer)
    lesson_attribute = db.Column(db.String(8))
    lesson_state = db.Column(db.String(8))
    lesson_level = db.Column(db.String(8))
    lesson_name = db.Column(db.String(32))
    lesson_teacher_id = db.Column(db.String(16))
    lesson_teacher_letter = db.Column(db.String(32))
    lesson_teacher_name = db.Column(db.String(8))
    lesson_teacher_unit = db.Column(db.String(16))
    lesson_unit = db.Column(db.String(16))
    lesson_year = db.Column(db.String(32))
    lesson_semester = db.Column(db.Integer)
    lesson_week = db.Column(db.String(48))
    lesson_time = db.Column(db.String(16))
    lesson_room = db.Column(db.String(16))
    lesson_class = db.Column(db.String(24))
    lesson_type = db.Column(db.String(8))
    lesson_weekday = db.Column(db.Integer)
    lesson_grade = db.Column(db.String(64))
    assgin_group = db.Column(db.String(8))
    lesson_attention_reason = db.Column(db.String(255))
    lesson_model = db.Column(db.Boolean)

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


class Lesson(object):
    def __init__(self):
        self.model = {
            'lesson_attribute':None,
            'lesson_state':None,
            'lesson_teacher_id':None,
            'lesson_name':None,
            'lesson_teacher_name':None,
            'lesson_semester':None,
            'lesson_level':None,
            'lesson_teacher_unit':None,
            'lesson_unit':None,
            'lesson_year':None,
            'lesson_type':None,
            'lesson_cases':[]
        }
        self.lesson_cases = []

    def lesson_case_to_dict(self):
        for id, data in enumerate(self.lesson_cases):
            try:
                data.id = id
                self.model['lesson_cases'].append(data.model)
            except:
                pass


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

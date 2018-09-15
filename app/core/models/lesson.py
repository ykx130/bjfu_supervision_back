from app.utils.mysql import db
from datetime import datetime


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.String(16), default="")
    lesson_attribute = db.Column(db.String(8), default="")
    lesson_state = db.Column(db.String(8), default="")
    lesson_level = db.Column(db.String(8), default="")
    lesson_name = db.Column(db.String(32), default="")
    lesson_teacher_id = db.Column(db.String(48), default="")
    lesson_teacher_letter = db.Column(db.String(32), default="")
    lesson_teacher_name = db.Column(db.String(8), default="")
    lesson_teacher_unit = db.Column(db.String(16), default="")
    lesson_unit = db.Column(db.String(16), default="")
    lesson_year = db.Column(db.String(32), default="")
    lesson_semester = db.Column(db.Integer, default="")
    lesson_class = db.Column(db.String(255), default="")
    lesson_type = db.Column(db.String(8), default="")
    lesson_grade = db.Column(db.String(64), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def lessons(condition):
        lesson_data = Lesson.query.filter(Lesson.using == True)
        for key, value in condition.items():
            if hasattr(Lesson, key):
                lesson_data = lesson_data.filter(getattr(Lesson, key) == value)
        return lesson_data

    @property
    def lesson_cases(self):
        return LessonCase.query.join(Lesson, LessonCase.lesson_id == Lesson.id).filter(
            LessonCase.lesson_id == self.id).filter(LessonCase.using == True)


class LessonCase(db.Model):
    __tablename__ = "lesson_cases"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.Integer, default=-1)
    lesson_room = db.Column(db.String(48), default="")
    lesson_weekday = db.Column(db.Integer, default=0)
    lesson_week = db.Column(db.String(48), default="")
    lesson_time = db.Column(db.String(48), default="")
    lesson_date = db.Column(db.Date, default=datetime.now())
    using = db.Column(db.Boolean, default=True)


class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(16))
    begin_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def terms(condition):
        terms_data = Term.query.filter(Term.using == True)
        for key, value in condition:
            if hasattr(Term, key):
                terms_data = terms_data.filter(getattr(Term, key) == value)
        if 'time' in condition:
            terms_data = terms_data.filter(Term.begin_time < condition['time']).filter(
                Term.end_time >= condition['time'])
        return terms_data


class SchoolTerm():
    def __init__(self, term_name=None):
        self.term_name = term_name

    def __add__(self, other):
        term_parts = self.term_name.split("-")
        term_future = 2 if (int(term_parts[2]) + other) % 2 == 0 else 1
        years = other / 2 if (int(term_parts[2]) == 1) else other / 2 + 1
        begin_year = (int(term_parts[0]) + years)
        end_year = (int(term_parts[1]) + years)
        return SchoolTerm(term_name="-".join([str(begin_year), str(end_year), str(term_future)]))


class NoticeLesson(db.Model):
    __tablename__ = 'notice_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.Integer, default=-1)
    assgin_group = db.Column(db.String(32), default="")
    term = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def notice_lessons(condition=None):
        lessons = Lesson.query.filter(Lesson.using == True)
        for key, value in condition.items():
            if hasattr(Lesson, key):
                lessons = lessons.filter(getattr(Lesson, key) == value)
        lesson_ids = [lesson.lesson_id for lesson in lessons]
        notice_lessons = NoticeLesson.query.filter(NoticeLesson.using == True).filter(
            NoticeLesson.lesson_id.in_(lesson_ids))
        for key, value in condition.items():
            if hasattr(NoticeLesson, key):
                notice_lessons = notice_lessons.filter(getattr(NoticeLesson, key) == value)
        return notice_lessons


class ModelLesson(db.Model):
    __tablename__ = 'model_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.Integer, default=-1)
    term = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def model_lessons(condition=None):
        lessons = Lesson.query.filter(Lesson.using == True)
        for key, value in condition.items():
            if hasattr(Lesson, key):
                lessons = lessons.filter(getattr(Lesson, key) == value)
        lesson_ids = [lesson.lesson_id for lesson in lessons]
        model_lessons = ModelLesson.query.filter(ModelLesson.using == True).filter(
            ModelLesson.lesson_id.in_(lesson_ids))
        for key, value in condition.items():
            if hasattr(ModelLesson, key):
                model_lessons = model_lessons.filter(getattr(ModelLesson, key) == value)
        return model_lessons

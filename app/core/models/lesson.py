from app.utils.mysql import db
from datetime import datetime
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)  # lesson_notice id 关注课程id
    lesson_id = db.Column(db.String(16), default="")  # 被关注课程的id
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
    lesson_model = db.Column(db.String(32), default="")
    term = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def lessons(condition):
        name_map = {'lessons': Lesson}
        url_condition = UrlCondition(condition)
        query = Lesson.query.filter(Lesson.using == True)
        query = process_query(query, url_condition, name_map, Lesson)
        return query

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
    lesson_date = db.Column(db.Date, default=datetime.now)
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
        name_map = {'terms': Term}
        url_condition = UrlCondition(condition)
        query = Term.query.filter(Term.using == True)
        if 'time' in condition:
            query = query.filter(Term.begin_time < condition['time']).filter(
                Term.end_time >= condition['time'])
        query = process_query(query, url_condition, name_map, Term)
        return query


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
    lesson_id = db.Column(db.String(32), default=-1)
    assign_group = db.Column(db.String(32), default="")
    term = db.Column(db.String(32), default="")
    status = db.Column(db.String(32), default="")
    votes = db.Column(db.Integer, default=0)
    notice_reason = db.Column(db.String(128), default="")
    notices = db.Column(db.Integer, default=0)
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def notice_lessons(condition=None):
        name_map = {'lessons': Lesson, 'notice_lessons': NoticeLesson}
        url_condition = UrlCondition(condition)
        query = NoticeLesson.query.filter(NoticeLesson.using == True).join(Lesson,
                                                                           Lesson.lesson_id == NoticeLesson.lesson_id)
        query = process_query(query, url_condition, name_map, NoticeLesson)
        return query


class ModelLesson(db.Model):
    __tablename__ = 'model_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.String(32), default="")
    term = db.Column(db.String(32), default="")
    status = db.Column(db.String(32), default="推荐课")  # 好评课 推荐课
    votes = db.Column(db.Integer, default=0)
    notices = db.Column(db.Integer, default=0)
    assign_group = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def model_lessons(condition=None):
        name_map = {'lessons': Lesson, 'model_lessons': ModelLesson}
        url_condition = UrlCondition(condition)
        query = ModelLesson.query.filter(ModelLesson.using == True).join(Lesson,
                                                                         Lesson.lesson_id == ModelLesson.lesson_id)
        query = process_query(query, url_condition, name_map, ModelLesson)
        return query


class LessonRecord(db.Model):
    __tablename__ = 'lesson_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    group_name = db.Column(db.String(64), nullable=False, default="")
    to_be_submitted = db.Column(db.Integer, nullable=False, default=0)
    has_submitted = db.Column(db.Integer, nullable=False, default=0)
    total_times = db.Column(db.Integer, nullable=False, default=0)
    using = db.Column(db.Boolean, nullable=True, default=True)

    @staticmethod
    def lesson_records(condition):
        name_map = {'lesson_records': LessonRecord}
        query = LessonRecord.query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(condition)
        query = process_query(query, url_condition, name_map, LessonRecord)
        return query

from app.utils.mysql import db
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query, count_query, page_query
from app.utils.Error import CustomError
from datetime import datetime
from app.utils.misc import convert_string_to_date
from sqlalchemy.sql import or_


class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(16))
    begin_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, term):
        if term is None:
            return None
        term_dict = {
            'name': term.name,
            'begin_time': str(term.begin_time),
            'end_time': str(term.end_time)
        }
        return term_dict

    @classmethod
    def reformatter_insert(cls, data):
        name = data.get('name', None)
        if name is None:
            raise CustomError(500, 200, 'name must be given')
        parts = name.split('-')
        if len(parts) != 3:
            raise CustomError(500, 200, 'name is wrong')
        year = int(parts[0])
        term_num = int(parts[2])
        if term_num == 1:
            begin_year = year
            end_year = year
            begin_date = '08-01'
            end_date = '02-15'
        else:
            begin_year = year
            end_year = year + 1
            begin_date = '02-15'
            end_date = '08-01'
        data['begin_time'] = convert_string_to_date(str(begin_year) + '-' + begin_date)
        data['end_time'] = convert_string_to_date(str(end_year) + '-' + end_date)
        return data

    @classmethod
    def reformatter_update(cls, data):
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Term.query
        if not unscoped:
            query = query.filter(Term.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Term)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def query_terms(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        url_condition = UrlCondition(query_dict)
        query = Term.query
        if not unscoped:
            query = query.filter(Term.using == True)
        if 'time' in query_dict:
            query = query.filter(Term.begin_time < query_dict['time']).filter(
                Term.end_time >= query_dict['time'])
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Term)
            (terms, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(term) for term in terms], total

    @classmethod
    def get_term(cls, term_name: str, unscoped: bool = False):
        term = Term.query
        if not unscoped:
            term = term.filter(Term.using == True)
        try:
            term = term.filter(Term.name == term_name).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(term)

    @classmethod
    def insert_term(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        term = Term()
        for key, value in data.items():
            if hasattr(term, key):
                setattr(term, key, value)
        db.session.add(term)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class LessonRecord(db.Model):
    __tablename__ = 'lesson_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    term = db.Column(db.String(32), default='')
    username = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    group_name = db.Column(db.String(64), nullable=False, default='')
    to_be_submitted = db.Column(db.Integer, nullable=False, default=0)
    has_submitted = db.Column(db.Integer, nullable=False, default=0)
    total_times = db.Column(db.Integer, nullable=False, default=0)
    using = db.Column(db.Boolean, nullable=True, default=True)

    @classmethod
    def formatter(cls, lesson_record):
        if lesson_record is None:
            return None
        try:
            lesson_record_dict = {
                'id': lesson_record.id,
                'username': lesson_record.username,
                'name': lesson_record.name,
                'term': lesson_record.term,
                'group_name': lesson_record.group_name,
                'to_be_submitted': lesson_record.to_be_submitted,
                'has_submitted': lesson_record.has_submitted,
                'total_times': lesson_record.total_times
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return lesson_record_dict

    @classmethod
    def reformatter_insert(cls, data):
        return data

    @classmethod
    def reformatter_update(cls, data):
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = LessonRecord.query
        if not unscoped:
            query = query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonRecord)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_lesson_record(cls, query_dict: dict, unscoped: bool = False):
        lesson_record = LessonRecord.query
        if not unscoped:
            lesson_record = lesson_record.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            lesson_record = process_query(lesson_record, url_condition.filter_dict, url_condition.sort_limit_dict,
                                          LessonRecord).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(lesson_record)

    @classmethod
    def insert_lesson_record(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        data = cls.reformatter_insert(data)
        lesson_record = LessonRecord()
        for key, value in data.items():
            if hasattr(lesson_record, key):
                setattr(lesson_record, key, value)
        db.session.add(lesson_record)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_lesson_records(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        query = LessonRecord.query
        if not unscoped:
            query = query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonRecord)
            (lesson_records, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(lesson_record) for lesson_record in lesson_records], total

    @classmethod
    def delete_lesson_record(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = dict()
        query = LessonRecord.query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonRecord)
            (lesson_records, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_record in lesson_records:
            lesson_record.using = False
            db.session.add(lesson_record)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_lesson_record(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = dict()
        if query_dict is None:
            query_dict = dict()
        data = cls.reformatter_update(data)
        query = LessonRecord.query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonRecord)
            (lesson_records, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_record in lesson_records:
            for key, value in data.items():
                if hasattr(lesson_record, key):
                    setattr(lesson_record, key, value)
            db.session.add(lesson_record)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class RawLesson(db.Model):
    __tablename__ = 'raw_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.String(255), default='')  # 被关注课程的id
    lesson_attribute = db.Column(db.String(255), default='')
    lesson_state = db.Column(db.String(255), default='')
    lesson_level = db.Column(db.String(255), default='')
    lesson_name = db.Column(db.String(255), default='')
    lesson_teacher_id = db.Column(db.String(255), default='')
    lesson_teacher_letter = db.Column(db.String(255), default='')
    lesson_teacher_name = db.Column(db.String(255), default='')
    lesson_teacher_unit = db.Column(db.String(255), default='')
    lesson_unit = db.Column(db.String(255), default='')
    lesson_year = db.Column(db.String(255), default='')
    lesson_semester = db.Column(db.Integer, default='')
    lesson_week = db.Column(db.String(255), default='')
    lesson_time = db.Column(db.String(255), default='')
    lesson_room = db.Column(db.String(255), default='')
    lesson_class = db.Column(db.String(255), default='')
    lesson_type = db.Column(db.String(255), default='')
    lesson_weekday = db.Column(db.String(255), default='')
    lesson_grade = db.Column(db.String(255), default='')
    assign_group = db.Column(db.String(255), default='')

    @classmethod
    def delete_all(cls):
        RawLesson.query.delete()

    @classmethod
    def insert(cls, data):
        raw_lesson = RawLesson()
        for key, value in data.items():
            if hasattr(raw_lesson, key):
                setattr(raw_lesson, key, value)
        db.session.add(raw_lesson)
        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)  # lesson_notice id 关注课程id
    raw_lesson_id = db.Column(db.String(32), default='')
    lesson_id = db.Column(db.String(32), default='')  # 被关注课程的id
    lesson_attribute = db.Column(db.String(8), default='')
    lesson_state = db.Column(db.String(8), default='')
    lesson_level = db.Column(db.String(8), default='')
    lesson_name = db.Column(db.String(32), default='')
    lesson_teacher_id = db.Column(db.String(48), default='')
    lesson_teacher_letter = db.Column(db.String(32), default='')
    lesson_teacher_name = db.Column(db.String(8), default='')
    lesson_teacher_unit = db.Column(db.String(16), default='')
    lesson_unit = db.Column(db.String(16), default='')
    lesson_year = db.Column(db.String(32), default='')
    lesson_semester = db.Column(db.Integer, default='')
    lesson_class = db.Column(db.String(255), default='')
    lesson_type = db.Column(db.String(8), default='')
    lesson_grade = db.Column(db.String(64), default='')
    lesson_model = db.Column(db.String(32), default='')
    term = db.Column(db.String(32), default='')
    notices = db.Column(db.Integer, default=0)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, lesson):
        if lesson is None:
            return None
        lesson_dict = {'id': lesson.id, 'lesson_id': lesson.lesson_id, 'lesson_attribute': lesson.lesson_attribute,
                       'lesson_state': lesson.lesson_state, 'lesson_teacher_id': lesson.lesson_teacher_id,
                       'lesson_name': lesson.lesson_name, 'lesson_teacher_name': lesson.lesson_teacher_name,
                       'lesson_semester': lesson.lesson_semester, 'lesson_level': lesson.lesson_level,
                       'lesson_teacher_unit': lesson.lesson_teacher_unit, 'lesson_unit': lesson.lesson_unit,
                       'lesson_year': lesson.lesson_year, 'lesson_type': lesson.lesson_type,
                       'lesson_class': lesson.lesson_class, 'lesson_grade': lesson.lesson_grade,
                       'lesson_model': lesson.lesson_model, 'term': lesson.term, 'notices': lesson.notices,
                       'raw_lesson_id': lesson.raw_lesson_id, }
        return lesson_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        allow_column = ['lesson_id', 'lesson_attribute', 'lesson_state', 'lesson_level', 'lesson_name',
                        'lesson_teacher_id', 'lesson_teacher_letter', 'lesson_teacher_name', 'lesson_teacher_unit',
                        'lesson_unit', 'lesson_year', 'lesson_semester', 'lesson_class', 'lesson_type', 'lesson_grade',
                        'lesson_model', 'term', 'notices', 'raw_lesson_id']
        new_data = dict()
        for key, value in data.items():
            if key in allow_column:
                new_data[key] = value
        return new_data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Lesson.query
        if not unscoped:
            query = query.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Lesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_lesson(cls, query_dict: dict, unscoped: bool = False):
        lesson = Lesson.query
        if not unscoped:
            lesson = lesson.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            lesson = process_query(lesson, url_condition.filter_dict, url_condition.sort_limit_dict,
                                   Lesson).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(lesson)

    @classmethod
    def insert_lesson(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        data = cls.reformatter_insert(data)
        lesson = Lesson()
        for key, value in data.items():
            if hasattr(lesson, key):
                setattr(lesson, key, value)
        db.session.add(lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_lessons(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Lesson.query
        if not unscoped:
            query = query.filter(Lesson.using == True)
        lesson_or_teacher_name = query_dict.get('lesson_or_teacher_name_or', None)
        if lesson_or_teacher_name is not None and len(lesson_or_teacher_name) != 0:
            del query_dict['lesson_or_teacher_name_or']
            lesson_or_teacher_name = lesson_or_teacher_name[0]
            query = query.filter(or_(Lesson.lesson_name.like(lesson_or_teacher_name + "%"),
                                     Lesson.lesson_teacher_name.like(lesson_or_teacher_name + "%")))
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Lesson)
            (lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(lesson) for lesson in lessons], total

    @classmethod
    def delete_lesson(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Lesson.query.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Lesson)
            (lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson in lessons:
            lesson.using = False
            db.session.add(lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_lesson(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Lesson.query.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Lesson)
            (lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson in lessons:
            for key, value in data.items():
                if hasattr(lesson, key):
                    setattr(lesson, key, value)
            db.session.add(lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_teacher_names(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Lesson.query.with_entities(Lesson.lesson_teacher_name).distinct()
        if not unscoped:
            query = query.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Lesson)
            (lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [data.lesson_teacher_name for data in query], total


class LessonCase(db.Model):
    __tablename__ = 'lesson_cases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.Integer, default=-1)
    lesson_room = db.Column(db.String(48), default='')
    lesson_weekday = db.Column(db.Integer, default=0)
    lesson_week = db.Column(db.String(48), default='')
    lesson_time = db.Column(db.String(48), default='')
    lesson_date = db.Column(db.Date, default=datetime.now)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, lesson_case):
        if lesson_case is None:
            return None
        lesson_case_dict = {'lesson_week': lesson_case.lesson_week, 'lesson_time': str(lesson_case.lesson_time),
                            'lesson_date': str(lesson_case.lesson_date.strftime('%Y-%m-%d')),
                            'lesson_weekday': lesson_case.lesson_weekday,
                            'lesson_room': lesson_case.lesson_room}
        return lesson_case_dict

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
        query = LessonCase.query
        if not unscoped:
            query = query.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonCase)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_lesson_case(cls, query_dict: dict, unscoped: bool = False):
        lesson_case = LessonCase.query
        if not unscoped:
            lesson_case = lesson_case.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            lesson_case = process_query(lesson_case, url_condition.filter_dict, url_condition.sort_limit_dict,
                                        LessonCase).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(lesson_case)

    @classmethod
    def insert_lesson_case(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        lesson_case = LessonCase()
        for key, value in data.items():
            if hasattr(lesson_case, key):
                setattr(lesson_case, key, value)
        db.session.add(lesson_case)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_lesson_cases(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = LessonCase.query
        if not unscoped:
            query = query.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonCase)
            (lesson_cases, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(lesson_case) for lesson_case in lesson_cases], total

    @classmethod
    def delete_lesson_case(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = LessonCase.query.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonCase)
            (lesson_cases, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_case in lesson_cases:
            lesson_case.using = False
            db.session.add(lesson_case)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_lesson_case(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = LessonCase.query.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, LessonCase)
            (lesson_cases, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_case in lesson_cases:
            for key, value in data.items():
                if hasattr(lesson_case, key):
                    setattr(lesson_case, key, value)
            db.session.add(lesson_case)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class NoticeLesson(db.Model):
    __tablename__ = 'notice_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.String(32), default=-1)
    group_name = db.Column(db.String(32), default='')
    term = db.Column(db.String(32), default='')
    lesson_attention_reason = db.Column(db.String(128), default='')
    unit = db.Column(db.String)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, notice_lesson):
        if notice_lesson is None:
            return None
        notice_lesson_dict = {
            'id': notice_lesson.id,
            'lesson_id': notice_lesson.lesson_id,
            'lesson_attention_reason': notice_lesson.lesson_attention_reason,
            'group_name': notice_lesson.group_name
        }
        return notice_lesson_dict

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
        query = NoticeLesson.query
        if not unscoped:
            query = query.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, NoticeLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_notice_lesson(cls, query_dict: dict, unscoped: bool = False):
        notice_lesson = NoticeLesson.query
        if not unscoped:
            notice_lesson = notice_lesson.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            notice_lesson = process_query(notice_lesson, url_condition.filter_dict, url_condition.sort_limit_dict,
                                          NoticeLesson).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(notice_lesson)

    @classmethod
    def insert_notice_lesson(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        notice_lesson = NoticeLesson()
        for key, value in data.items():
            if hasattr(notice_lesson, key):
                setattr(notice_lesson, key, value)
        db.session.add(notice_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_notice_lessons(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}

        query = NoticeLesson.query
        if not unscoped:
            query = query.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, NoticeLesson)
            (notice_lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(notice_lesson) for notice_lesson in notice_lessons], total

    @classmethod
    def delete_notice_lesson(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = NoticeLesson.query.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, NoticeLesson)
            (notice_lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for notice_lesson in notice_lessons:
            notice_lesson.using = False
            db.session.add(notice_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_notice_lesson(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = NoticeLesson.query.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, NoticeLesson)
            (notice_lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for notice_lesson in notice_lessons:
            for key, value in data.items():
                if hasattr(notice_lesson, key):
                    setattr(notice_lesson, key, value)
            db.session.add(notice_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class ModelLesson(db.Model):
    __tablename__ = 'model_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.String(32), default='')
    term = db.Column(db.String(32), default='')
    status = db.Column(db.Integer, default=2)  # 好评课 推荐课
    votes = db.Column(db.Integer, default=0)
    group_name = db.Column(db.String(32), default='')
    is_lock = db.Column(db.Integer, default=0)  # 锁定 未锁定
    using = db.Column(db.Boolean, default=True)
    unit = db.Column(db.String)
    guiders = db.Column(db.JSON, default=[])

    @classmethod
    def formatter(cls, model_lesson):
        if model_lesson is None:
            return None
        status_dict = {1: '推荐为好评课', 2: '待商榷'}
        status = status_dict[model_lesson.status]
        model_lesson_dict = {
            'id': model_lesson.id,
            'lesson_id': model_lesson.lesson_id,
            'group_name': model_lesson.group_name,
            'status': status,
            'votes': model_lesson.votes,
            'is_lock': model_lesson.is_lock,
            'guiders': model_lesson.guiders
        }
        return model_lesson_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        allow_column = ['lesson_id', 'group_name', 'status', 'votes', 'term', 'unit', 'guiders']
        status_dict = {'推荐为好评课': 1, '待商榷': 2}
        new_data = dict()
        for key, value in data.items():
            if key in allow_column:
                if key == 'status':
                    value = status_dict[value]
                new_data[key] = value
        return new_data

    @classmethod
    def reformatter_update(cls, data: dict):
        if data is None:
            return dict()
        new_data = dict()
        status_dict = {'推荐为好评课': 1, '待商榷': 2}
        for key, value in data.items():
            if key == 'status':
                value = status_dict[value]
            new_data[key] = value
        return new_data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ModelLesson.query
        if not unscoped:
            query = query.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ModelLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_model_lesson(cls, query_dict: dict, unscoped: bool = False):
        model_lesson = ModelLesson.query
        if not unscoped:
            model_lesson = model_lesson.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            model_lesson = process_query(model_lesson, url_condition.filter_dict, url_condition.sort_limit_dict,
                                         ModelLesson).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(model_lesson)

    @classmethod
    def get_model_lesson_by_lesson_id(cls, query_dict: dict, unscoped: bool = False):
        model_lesson = ModelLesson.query
        if not unscoped:
            model_lesson = model_lesson.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            model_lesson = process_query(model_lesson, url_condition.filter_dict, url_condition.sort_limit_dict,
                                         ModelLesson).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(model_lesson)

    @classmethod
    def insert_model_lesson(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        print(data)
        data = cls.reformatter_insert(data)
        print(data)
        model_lesson = ModelLesson()
        for key, value in data.items():
            if hasattr(model_lesson, key):
                setattr(model_lesson, key, value)
        db.session.add(model_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_model_lessons(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ModelLesson.query
        if not unscoped:
            query = query.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ModelLesson)
            (model_lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(model_lesson) for model_lesson in model_lessons], total

    @classmethod
    def delete_model_lesson(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = ModelLesson.query.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ModelLesson)
            (model_lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for model_lesson in model_lessons:
            model_lesson.using = False
            db.session.add(model_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_model_lesson(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = ModelLesson.query.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, ModelLesson)
            (model_lessons, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for model_lesson in model_lessons:
            for key, value in data.items():
                if hasattr(model_lesson, key):
                    setattr(model_lesson, key, value)
            db.session.add(model_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

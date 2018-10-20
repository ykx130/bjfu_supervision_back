from app.utils.mysql import db


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
        lesson_record_data = LessonRecord.query
        for key, value in condition:
            if hasattr(LessonRecord, key):
                lesson_record_data = lesson_record_data.filter(getattr(LessonRecord, key) == value)
        return lesson_record_data

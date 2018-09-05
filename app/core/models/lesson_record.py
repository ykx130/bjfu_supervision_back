from app import db


class LessonRecord(db.Model):
    __tablename__ = 'lesson_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    group_id = db.Column(db.Integer, nullable=False, default=-1)
    to_be_submitted = db.Column(db.Integer, nullable=False, default=0)
    has_submitted = db.Column(db.Integer, nullable=False, default=0)
    total_times = db.Column(db.Integer, nullable=False, default=0)

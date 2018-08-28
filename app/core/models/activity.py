from app import db
from datetime import datetime
from app.core.models.user import User


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), default="")
    teacher = db.Column(db.String(64), default="")
    start_time = db.Column(db.TIMESTAMP, default=datetime.now())
    end_time = db.Column(db.TIMESTAMP, default=datetime.now())
    place = db.Column(db.String(128), default="")
    state = db.Column(db.String(16), default="")
    information = db.Column(db.String(128), default="")
    all_num = db.Column(db.Integer, default=0)
    attend_num = db.Column(db.Integer, default=0)
    remainder_num = db.Column(db.Integer, default=0)
    term = db.Column(db.String(32), default="")
    apply_start_time = db.Column(db.TIMESTAMP, default=datetime.now())
    apply_end_time = db.Column(db.TIMESTAMP, default=datetime.now())
    apply_state = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def activities(condition):
        activity_datas = Activity.query.outerjoin(ActivityUser, ActivityUser.activity_id == Activity.id).outerjoin(User,
                                                                                                                   User.username == ActivityUser.username).filter(
            Activity.using == True)
        for key, value in condition.items():
            if hasattr(Activity, key):
                activity_datas = activity_datas.filter(getattr(Activity, key) == value)
        return activity_datas

    @property
    def activity_users(self):
        datas = User.query.join(ActivityUser, ActivityUser.username == User.username).join(Activity,
                                                                                           Activity.id == ActivityUser.activity_id).filter(
            ActivityUser.using == True).filter(Activity.using == True).filter(User.using == True).filter(
            Activity.id == self.id)
        return datas


class ActivityUser(db.Model):
    __tablename__ = 'activity_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default="")
    activity_id = db.Column(db.Integer, default=-1)
    state = db.Column(db.String(16), default="")
    fin_state = db.Column(db.String(16), default="")
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def activity_user_state(id, username):
        data = ActivityUser.query.join(Activity, Activity.id == ActivityUser.activity_id).join(User,
                                                                                               User.username == ActivityUser.username).filter(
            User.username == username).filter(Activity.id == id).filter(ActivityUser.using == True).filter(
            Activity.using == True).filter(User.using == True).first()
        return data

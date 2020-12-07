from app.utils.mysql import db
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query, count_query, page_query
from app.utils.Error import CustomError
from app.utils.misc import convert_string_to_datetime, convert_datetime_to_string
from datetime import datetime


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    title = db.Column(db.String(64), default='')
    presenter = db.Column(db.String(64), default='')
    module = db.Column(db.String(64), default='')
    start_time = db.Column(db.TIMESTAMP, default=datetime.now)
    place = db.Column(db.String(128), default='')
    apply_state = db.Column(db.String(16), default='')
    organizer = db.Column(db.String(64), default='')
    all_num = db.Column(db.Integer, default=0)
    attend_num = db.Column(db.Integer, default=0)
    remainder_num = db.Column(db.Integer, default=0)
    term = db.Column(db.String(32), default='')
    period = db.Column(db.Integer, default=0)
    is_obligatory=db.Column(db.Boolean, default=False)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, activity):
        if activity is None:
            return None
        try:
            activity_dict = {
                'id': activity.id,
                'title': activity.title,
                'presenter': activity.presenter,
                'module':activity.module,
                'start_time': convert_datetime_to_string(activity.start_time),
                'place': activity.place,
                'apply_state': activity.apply_state,
                'organizer': activity.organizer,
                'all_num':activity.all_num,
                'attend_num': activity.attend_num,
                'remainder_num': activity.remainder_num,
                'term': activity.term,
                'period':activity.period,
                'is_obligatory': activity.is_obligatory
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Activity.query
        if not unscoped:
            query = query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, Activity)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_activity(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        activity = Activity()
        for key, value in data.items():
            if hasattr(activity, key):
                setattr(activity, key, value)
        db.session.add(activity)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_activity(cls, query_dict: dict, unscoped: bool = False):
        activity = Activity.query
        if not unscoped:
            activity = activity.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            activity = process_query(activity, url_condition.filter_dict, url_condition.sort_limit_dict,
                                     Activity).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(activity)

    @classmethod
    def query_activities(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Activity.query
        if not unscoped:
            query = query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Activity)
            (activities, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(activity) for activity in activities], total

    @classmethod
    def delete_activity(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Activity.query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Activity)
            (activities, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity in activities:
            activity.using = False
            db.session.add(activity)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_activity(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Activity.query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Activity)
            (activities, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity in activities:
            for key, value in data.items():
                if hasattr(activity, key):
                    setattr(activity, key, value)
            db.session.add(activity)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class ActivityUser(db.Model):
    __tablename__ = 'activity_users'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    username = db.Column(db.String(64), default='')
    activity_id = db.Column(db.Integer, default=-1)
    state = db.Column(db.String(16), default='')
    fin_state = db.Column(db.String(16), default='')
    activity_type = db.Column(db.String(64), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, activity_user_user):
        if activity_user_user is None:
            return None
        try:
            activity_user_user_dict = {
                'id': activity_user_user.id,
                'username': activity_user_user.username,
                'activity_id': activity_user_user.activity_id,
                # 'activity_user_id': activity_user_user.id,
                'state': activity_user_user.state,
                'fin_state': activity_user_user.fin_state,
                'activity_type':activity_user_user.activity_type
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_user_user_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ActivityUser.query
        if not unscoped:
            query = query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, ActivityUser)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_activity_user(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        activity_user = ActivityUser()
        for key, value in data.items():
            if hasattr(activity_user, key):
                setattr(activity_user, key, value)
        db.session.add(activity_user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_activity_user(cls, query_dict: dict, unscoped: bool = False):
        activity_user = ActivityUser.query
        if not unscoped:
            activity_user = activity_user.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            activity_user = process_query(activity_user, url_condition.filter_dict, url_condition.sort_limit_dict,
                                          ActivityUser).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(activity_user)

    @classmethod
    def query_activity_users(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ActivityUser.query
        if not unscoped:
            query = query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, ActivityUser)
            (activity_users, total) = page_query(
                query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(activity_user) for activity_user in activity_users], total

    @classmethod
    def delete_activity_user(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = ActivityUser.query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, ActivityUser)
            (activity_users, total) = page_query(
                query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_user in activity_users:
            activity_user.using = False
            db.session.add(activity_user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_activity_user(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = ActivityUser.query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, ActivityUser)
            (activity_users, total) = page_query(
                query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_user in activity_users:
            for key, value in data.items():
                if hasattr(activity_user, key):
                    setattr(activity_user, key, value)
            db.session.add(activity_user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

class ActivityPlan(db.Model):
    __tablename__ = 'activity_plan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    period = db.Column(db.Integer, nullable=False, default=0)
    min_worktime = db.Column(db.Integer, nullable=False, default=0)
    max_worktime = db.Column(db.Integer, nullable=False, default=0)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, activity_plan):
        if activity_plan is None:
            return None
        try:
            activity_plan_dict = {
                'id': activity_plan.id,
                'period': activity_plan.period,
                'min_worktime': activity_plan.min_worktime,
                'max_worktime': activity_plan.max_worktime,
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_plan_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def insert_activity_plan(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        data = cls.reformatter_insert(data)
        activity_plan = ActivityPlan()
        for key, value in data.items():
            if hasattr(activity_plan, key):
                setattr(activity_plan, key, value)
        db.session.add(activity_plan)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_activity_plan(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        query = ActivityPlan.query
        if not unscoped:
            query = query.filter(ActivityPlan.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                                      ActivityPlan)
            (res, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in res], total

    @classmethod
    def get_activity_plan(cls, query_dict: dict, unscoped: bool = False):
        activity_plan = ActivityPlan.query
        if not unscoped:
            activity_plan = activity_plan.filter(ActivityPlan.using == True)
        url_condition =UrlCondition(query_dict)
        try:
            activity_plan = process_query(activity_plan, url_condition.filter_dict,
                                                          url_condition.sort_limit_dict,
                                                          ActivityPlan).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(activity_plan)

    @classmethod
    def delete_activity_plan(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = dict()
        query = ActivityPlan.query.filter(ActivityPlan.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict,
                                                      url_condition.sort_limit_dict, ActivityPlan)
            (activity_plans, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_plan in activity_plans:
            activity_plan.using = False
            db.session.add(activity_plan)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_activity_plan(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = dict()
        if query_dict is None:
            query_dict = dict()
        data = cls.reformatter_update(data)
        query = ActivityPlan.query.filter(ActivityPlan.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                                      ActivityPlan)
            (activity_plans, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_plan in activity_plans:
            for key, value in data.items():
                if hasattr(activity_plan, key):
                    setattr(activity_plan, key, value)
            db.session.add(activity_plan)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

class Competition(db.Model):
    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    award_name = db.Column(db.String(64), default='')
    organizer = db.Column(db.String(64), default='')
    level = db.Column(db.String(64), default='')
    award_time = db.Column(db.TIMESTAMP, default=datetime.now)
    term = db.Column(db.String(32), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, competition):
        if competition is None:
            return None
        try:
            competition_dict = {
                'id': competition.id,
                'award_name': competition.award_name,
                'organizer': competition.organizer,
                'level': competition.level,
                'award_time': convert_datetime_to_string(competition.award_time),
                'term': competition.term
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return competition_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Competition.query
        if not unscoped:
            query = query.filter(Competition.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, Competition)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_competition(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        competition = Competition()
        for key, value in data.items():
            if hasattr(competition, key):
                setattr(competition, key, value)
        db.session.add(competition)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_competition(cls, query_dict: dict, unscoped: bool = False):
        competition = Competition.query
        if not unscoped:
            competition = competition.filter(Competition.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            competition = process_query(competition, url_condition.filter_dict, url_condition.sort_limit_dict,
                                     Competition).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(competition)

    @classmethod
    def query_competitions(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Competition.query
        if not unscoped:
            query = query.filter(Competition.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Competition)
            (competitions, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(competition) for competition in competitions], total

    @classmethod
    def delete_competition(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Competition.query.filter(Competition.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Competition)
            (competitions, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for competition in competitions:
            competition.using = False
            db.session.add(competition)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_competition(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Competition.query.filter(Competition.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict,Competition)
            (competitions, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for competition in competitions:
            for key, value in data.items():
                if hasattr(competition, key):
                    setattr(competition, key, value)
            db.session.add(competition)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

class Exchange(db.Model):
    __tablename__ = 'exchange'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    invited_university = db.Column(db.String(64), default='')
    title = db.Column(db.String(64), default='')
    number =db.Column(db.Integer, default=0)
    exchange_time = db.Column(db.TIMESTAMP, default=datetime.now)
    term = db.Column(db.String(32), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, exchange):
        if exchange is None:
            return None
        try:
            exchange_dict = {
                'id': exchange.id,
                'invited_university': exchange.invited_university,
                'title': exchange.title,
                'number': exchange.number,
                'exchange_time': convert_datetime_to_string(exchange.exchange_time),
                'term': exchange.term
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return exchange_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Exchange.query
        if not unscoped:
            query = query.filter(Exchange.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, Exchange)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_exchange(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        exchange = Exchange()
        for key, value in data.items():
            if hasattr(exchange, key):
                setattr(exchange, key, value)
        db.session.add(exchange)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_exchange(cls, query_dict: dict, unscoped: bool = False):
        exchange = Exchange.query
        if not unscoped:
            exchange = exchange.filter(Exchange.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            exchange = process_query(exchange, url_condition.filter_dict, url_condition.sort_limit_dict,
                                     Exchange).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(exchange)

    @classmethod
    def query_exchanges(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Exchange.query
        if not unscoped:
            query = query.filter(Exchange.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Exchange)
            (exchanges, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(exchange) for exchange in exchanges], total

    @classmethod
    def delete_exchange(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Exchange.query.filter(Exchange.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Exchange)
            (exchanges, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for exchange in exchanges:
            exchange.using = False
            db.session.add(exchange)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_exchange(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Exchange.query.filter(Exchange.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict,Exchange)
            (exchanges, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for exchange in exchanges:
            for key, value in data.items():
                if hasattr(exchange, key):
                    setattr(exchange, key, value)
            db.session.add(exchange)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

class Research(db.Model):
    __tablename__ = 'research'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    author = db.Column(db.String(64), default='')
    title = db.Column(db.String(64), default='')
    journal = db.Column(db.String(64), default='')
    publication_time = db.Column(db.TIMESTAMP, default=datetime.now)
    term = db.Column(db.String(32), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, research):
        if research is None:
            return None
        try:
            research_dict = {
                'id': research.id,
                'author': research.author,
                'title': research.title,
                'journal': research.journal,
                'publication_time': convert_datetime_to_string(research.publication_time),
                'term': research.term
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return research_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Research.query
        if not unscoped:
            query = query.filter(Research.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, Research)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_research(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        research = Research()
        for key, value in data.items():
            if hasattr(research, key):
                setattr(research, key, value)
        db.session.add(research)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_research(cls, query_dict: dict, unscoped: bool = False):
        research = Research.query
        if not unscoped:
            research = research.filter(Exchange.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            research = process_query(research, url_condition.filter_dict, url_condition.sort_limit_dict,
                                     Research).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(research)

    @classmethod
    def query_researchs(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Exchange.query
        if not unscoped:
            query = query.filter(Research.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Research)
            (researchs, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(research) for research in researchs], total

    @classmethod
    def delete_research(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Research.query.filter(Research.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Research)
            (researchs, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for research in researchs:
            research.using = False
            db.session.add(research)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_research(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Research.query.filter(Research.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict,Research)
            (researchs, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for research in researchs:
            for key, value in data.items():
                if hasattr(research, key):
                    setattr(research, key, value)
            db.session.add(research)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    title = db.Column(db.String(64), default='')
    level = db.Column(db.String(64), default='')
    superior_units = db.Column(db.String(64), default='')
    start_time = db.Column(db.TIMESTAMP, default=datetime.now)
    end_time = db.Column(db.TIMESTAMP, default=datetime.now)
    leader = db.Column(db.String(128), default='')
    term = db.Column(db.String(32), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, project):
        if project is None:
            return None
        try:
            activity_dict = {
                'id': project.id,
                'title': project.title,
                'level': project.level,
                'superior_units':project.superior_units,
                'start_time': convert_datetime_to_string(project.start_time),
                'end_time': convert_datetime_to_string(project.end_time),
                'leader': project.place,
                'term': project.term
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Project.query
        if not unscoped:
            query = query.filter(Project.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, Project)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_project(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        project = Project()
        for key, value in data.items():
            if hasattr(project, key):
                setattr(project, key, value)
        db.session.add(project)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_project(cls, query_dict: dict, unscoped: bool = False):
        project = Project.query
        if not unscoped:
            project = project.filter(Project.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            project = process_query(project, url_condition.filter_dict, url_condition.sort_limit_dict,
                                     Project).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(project)

    @classmethod
    def query_projects(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Project.query
        if not unscoped:
            query = query.filter(Project.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Project)
            (projects, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(project) for project in projects], total

    @classmethod
    def delete_project(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Project.query.filter(Project.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Project)
            (projects, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for project in projects:
            project.using = False
            db.session.add(project)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_project(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Project.query.filter(Project.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Project)
            (projects, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for project in projects:
            for key, value in data.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            db.session.add(project)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True
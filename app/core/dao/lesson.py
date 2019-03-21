from app.utils.mysql import db
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query
from app.utils.Error import CustomError


class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(16))
    begin_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, term):
        term_dict = {
            'name': term.name,
            'begin_time': str(term.begin_time),
            'end_time': str(term.end_time)
        }
        return term_dict

    @classmethod
    def query_terms(cls, query_dict: dict = None):
        name_map = {'terms': Term}
        url_condition = UrlCondition(query_dict)
        query = Term.query.filter(Term.using == True)
        if 'time' in query_dict:
            query = query.filter(Term.begin_time < query_dict['time']).filter(
                Term.end_time >= query_dict['time'])
        try:
            (query, total) = process_query(query, url_condition.filter_dict,
                                           url_condition.sort_limit_dict, url_condition.page_dict,
                                           name_map, Term)
        except Exception as e:
            return None, None, CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total, None

    @classmethod
    def get_term(cls, term_name):
        try:
            term = Term.query.filter(Term.name == term_name).first()
        except Exception as e:
            return None, CustomError(500, 500, str(e))
        if term is None:
            return None, CustomError(404, 404, 'term not found')
        return cls.formatter(term), None

    @classmethod
    def get_now_term(cls):
        try:
            term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first()
        except Exception as e:
            return None, CustomError(500, 500, str(e))
        if term is None:
            return None, CustomError(404, 404, 'term not found')
        return cls.formatter(term), None

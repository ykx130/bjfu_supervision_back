import app.core.dao as dao
from app.utils import CustomError, db
import app.core.services as service


class FormMetaController(object):

    @classmethod
    def get_form_meta(cls, query_dict):
        form_meta = dao.FormMeta.get_form_meta(query_dict=query_dict)
        if form_meta is None:
            raise CustomError(404, 404, 'form_meta not found')
        return form_meta

    @classmethod
    def query_form_metas(cls, query_dict: dict = None):
        if query_dict is None:
            query_dict = {'using': [True]}
        else:
            query_dict['using'] = [True]
        query_dict['_sort'] = ['order']
        return dao.FormMeta.query_form_metas(query_dict)

    @classmethod
    def get_history_form_meta(cls, name: str = None, query_dict: dict = None):
        if query_dict is None:
            query_dict = dict()
        if name is None:
            raise CustomError(500, 200, 'name must be given')
        if query_dict is None:
            query_dict = {'name': [name]}
        else:
            query_dict['name'] = [name]
        (form_metas, total) = dao.FormMeta.query_form_metas(query_dict)
        return form_metas, total

    @classmethod
    def query_form_meta_history(cls, query_dict: dict = None):
        if query_dict is None:
            query_dict = dict()
        return dao.FormMeta.query_form_metas(query_dict)

    @classmethod
    def insert_form_meta(cls, data: dict = None):
        if data is None:
            data = dict()
        name = data.get('name', '')
        (_, num) = dao.FormMeta.query_form_metas(query_dict={'name': name}, unscoped=False)
        if num != 0:
            raise CustomError(500, 200, 'name has been used')
        return dao.FormMeta.insert_form_meta(data)

    @classmethod
    def delete_form_meta(cls, name: str = None, version: str = None):
        query_dict = {'name': name}
        if version is not None:
            query_dict.update({'version': version})
        form_meta = dao.FormMeta.get_form_meta(query_dict)
        if form_meta is None:
            raise CustomError(404, 404, 'form_meta not found')
        return dao.FormMeta.delete_form_meta({'name': name, 'version': version})

    @classmethod
    def update_form_meta(cls, name: str = None, data: dict = None):
        if data is None:
            data = dict()
        form_meta = dao.FormMeta.get_form_meta(query_dict={'name': name})
        if form_meta is None:
            raise CustomError(404, 404, 'form_meta not found')
        dao.FormMeta.delete_form_meta({'name': name, 'version': form_meta['version']})
        dao.FormMeta.insert_form_meta(data)
        return True


class WorkPlanController(object):

    @classmethod
    def formatter(cls, work_plan):
        return work_plan

    @classmethod
    def reformatter_insert(cls, data: dict):
        if 'form_meta_name' not in data:
            raise CustomError(500, 200, 'form meta name should be given')
        if 'form_meta_version' not in data:
            raise CustomError(500, 200, 'form meta version  should be given')
        return data

    @classmethod
    def get_work_plan(cls, query_dict: dict, unscoped: bool = False):
        work_plan = dao.WorkPlan.get_work_plan(query_dict=query_dict, unscoped=unscoped)
        if work_plan is None:
            raise CustomError(404, 404, 'work_plan not found')
        return cls.formatter(work_plan)

    @classmethod
    def query_work_plan(cls, query_dict: dict, unscoped: bool = False):
        (work_plans, num) = dao.WorkPlan.query_work_plan(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(work_plan) for work_plan in work_plans], num

    @classmethod
    def delete_work_plan(cls, ctx: bool = True, id: int = 0):
        work_plan = dao.WorkPlan.get_work_plan(query_dict={'id': id}, unscoped=False)
        if work_plan is None:
            raise CustomError(404, 404, 'work_plan not found')
        try:
            dao.WorkPlan.delete_work_plan(ctx=False, query_dict={'id': [id]})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_work_plan(cls, ctx: bool = True, id: int = 0, data: dict = None):
        if data is None:
            data = dict()
        work_plan = dao.WorkPlan.get_work_plan(query_dict={'id': id}, unscoped=False)
        if work_plan is None:
            raise CustomError(404, 404, 'work_plan not found')
        try:
            dao.WorkPlan.update_work_plan(ctx=False, query_dict={'id': [id]}, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def insert_work_plan(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        data = cls.reformatter_insert(data)
        (form_meta, num) = dao.FormMeta.query_form_metas(
            query_dict={'name': [data['form_meta_name']], 'version': [data['form_meta_version']],
                        'using': [True]})
        if num == 0:
            raise CustomError(404, 404, 'form_meta not found')
        try:
            dao.WorkPlan.insert_work_plan(ctx=ctx, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_work_plan_detail(cls, query_dict, unscoped=False):
        if query_dict.get('term', None):
            term = service.TermService.get_now_term()['name']
            query_dict.update({'term': term})
        (work_plans, num) = dao.WorkPlan.query_work_plan(query_dict=query_dict)
        results = list()
        for work_plan in work_plans:
            form_meta = dao.FormMeta.get_form_meta(query_dict={'name': work_plan['form_meta_name'],
                                                               'version': work_plan['form_meta_version'],},
                                                   unscoped=unscoped)
            if form_meta is None:
                raise CustomError(404, 404, 'form_meta not found')
            work_plan['form_meta'] = form_meta
            results.append(work_plan)
        results.sort(key=lambda x: x.get('form_meta', {}).get('order', 1) )
        return results, num

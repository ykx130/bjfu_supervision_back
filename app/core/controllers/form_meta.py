import app.core.dao as dao
from app.utils import CustomError


class FormMetaController(object):

    @classmethod
    def get_form_meta(cls, name: str = None, version: str = None):
        return dao.FormMeta.get_form_meta(name, version)

    @classmethod
    def query_form_meta(cls, query_dict: dict = None):
        if query_dict is None:
            query_dict = {'using': [True]}
        else:
            query_dict['using'] = [True]
        return dao.FormMeta.query_form_meta(query_dict)

    @classmethod
    def get_history_form_meta(cls, name: str = None, query_dict: dict = None):
        if name is None:
            raise CustomError(500, 200, 'name must be given')
        if query_dict is None:
            query_dict = {'name': [name]}
        else:
            query_dict['name'] = [name]
        (form_metas, total, err) = dao.FormMeta.query_form_meta(query_dict)
        return form_metas, total

    @classmethod
    def query_form_meta_history(cls, query_dict: dict = None):
        return dao.FormMeta.query_form_meta(query_dict)

    @classmethod
    def insert_form_meta(cls, data: dict = None):
        return dao.FormMeta.insert_form_meta(data)

    @classmethod
    def delete_form_meta(cls, where_dict: dict = None):
        return dao.FormMeta.delete_form_meta(where_dict)

    @classmethod
    def update_form_meta(cls, name: str = None, data: dict = None):
        form_meta = dao.FormMeta.get_form_meta(name)
        ifSuccess = dao.FormMeta.delete_form_meta({'name': name, 'version': form_meta['version']})
        ifSuccess = dao.FormMeta.insert_form_meta(data)
        return ifSuccess


class WorkPlanController(object):

    @classmethod
    def get_work_plan(cls, id: int):
        return dao.WorkPlan.get_work_plan(id)

    @classmethod
    def query_work_plan(cls, query_dict: dict = None):
        return dao.WorkPlan.query_work_plan(query_dict)

    @classmethod
    def delete_work_plan(cls, id: int):
        return dao.WorkPlan.delete_work_plan(id)

    @classmethod
    def update_work_plan(cls, id: int, data: dict):
        return dao.WorkPlan.update_work_plan(id, data)

    @classmethod
    def insert_work_plan(cls, data: dict = None):
        form_meta_name = data['form_meta_name'] if 'form_meta_name' in data else None
        if form_meta_name is None:
            raise CustomError(500, 200, 'form_meta_name must be given')
        form_meta_version = data['form_meta_version'] if 'form_meta_version' in data else None
        if form_meta_version is None:
            raise CustomError(500, 200, 'form_meta_version must be given')
        condition = {'form_meta_name': [form_meta_name], 'form_meta_version': [form_meta_version], 'using': [True]}
        form_meta, num = dao.FormMeta.query_form_meta(condition)
        if num == 0:
            raise CustomError(404, 404, 'form_meta not found')
        ifSuccess = dao.WorkPlan.insert_work_plan(data)
        return ifSuccess

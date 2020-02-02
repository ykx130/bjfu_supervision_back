import app.core.dao as dao
from app.utils.Error import CustomError
from flask_login import current_user
import pandas
import app.core.services as service
class OtherModelLessonController(object):
    @classmethod
    def formatter(cls, other_model_lesson):
        if other_model_lesson is None:
            return None
        print(other_model_lesson)
        other_model_lesson_dict = {
            'id': other_model_lesson['id'],
            'group_name': other_model_lesson['group_name'],
            'lesson_name': other_model_lesson['lesson_name'],
            'lesson_attribute': other_model_lesson['lesson_attribute'],
            'term': other_model_lesson['term'],
            'lesson_teacher_name': other_model_lesson['lesson_teacher_name'],
            'unit': other_model_lesson['unit'],
            'using': other_model_lesson['using']
        }
        return other_model_lesson_dict

    @classmethod
    def query_other_model_lessons(cls, query_dict: dict, unscoped: bool = False):
        other_model_lessons, num = dao.OtherModelLesson.query_other_model_lessons(query_dict=query_dict, unscoped=unscoped)
        print(other_model_lessons)
        return [cls.formatter(other_model_lesson) for other_model_lesson in other_model_lessons],num

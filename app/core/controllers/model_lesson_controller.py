from app.core.services import model_lesson_service
from app.core.services import lesson_service


def find_model_lesson(id):
    (model_lesson, err) = model_lesson_service.find_model_lesson(id)
    if err is not None:
        return None, err
    (lesson, err) = lesson_service.find_lesson(model_lesson.lesson_id)
    if err is not None:
        return None, err
    (model, err) = model_lesson_service.model_lesson_dict(lesson, model_lesson)
    if err is not None:
        return None, err
    return model, None


def find_model_lessons(condition):
    (model_lessons, num, err) = model_lesson_service.find_model_lessons(condition)
    if err is not None:
        return None, None, err
    models = list()
    for model_lesson in model_lessons:
        (lesson, err) = lesson_service.find_lesson(model_lesson.lesson_id)
        if err is not None:
            return None, None, err
        (model, err) = model_lesson_service.model_lesson_dict(lesson, model_lesson)
        if err is not None:
            return None, None, err
        models.append(model)
    return models, num, None



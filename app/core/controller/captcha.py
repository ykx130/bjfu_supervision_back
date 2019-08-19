import os
from app.core.services import CaptchaService


class CaptchaController():
    @classmethod
    def new_captcha(cls):
        if not os.path.exists('static/captcha'):
            os.mkdir('static/captcha')
        (id, path) = CaptchaService.save('static/captcha')
        return id, path

from captcha.image import *
from app.config import *
from app import redis_cli
from app.utils import CustomError
import uuid
import time
import random
import string
import datetime
import os


class CaptchaService(object):
    @classmethod
    def make_uuid(cls):
        id = str(uuid.uuid1())
        return id

    @classmethod
    def make_code(cls):
        return ''.join(random.sample(string.ascii_letters + string.digits, 4))

    @classmethod
    def judge(cls, input: str, code: bytes):
        return input.lower() == str(code, encoding="utf8").lower()

    @classmethod
    def remove(cls, id: str):
        redis_cli.delete(id)

    @classmethod
    def make_image(cls, code, file_dir):
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        image = ImageCaptcha()
        unix_time = int(time.time())
        filename = str(unix_time) + '.' + 'png'
        file_path = os.path.join(file_dir, filename)
        image.write(code, file_path)
        return file_path

    @classmethod
    def save(cls, file_dir):
        code = cls.make_code()
        id = cls.make_uuid()
        path = cls.make_image(code, file_dir)
        redis_cli.set(id, code, ex=Config.CAPTCHA_EXPIRE)
        return id, path

    @classmethod
    def verify(cls, id: str, input: str):
        code = redis_cli.get(id)
        cls.remove(id)
        if code is None:
            raise CustomError(code=500, status_code=200, err_info="验证码失效")
        if cls.judge(input, code):
            return True
        else:
            return False

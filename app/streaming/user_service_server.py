from app.core.services import user_service
from app import app

if __name__ == '__main__':
    ctx = app.app_context()
    ctx.push()
    user_service.user_service_server()
from app.core.services import user_service
from app import app
import threading

if __name__ == '__main__':
    threading.local()
    ctx = app.app_context()
    ctx.push()
    user_service.user_service_server()

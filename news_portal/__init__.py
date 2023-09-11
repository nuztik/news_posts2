from .celery import app as celery_app

#настройка celery
__all__ = ('celery_app',)
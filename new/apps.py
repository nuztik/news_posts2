from django.apps import AppConfig


class NewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'new'

    def ready(self, signals=None, new=None):
        from .signals import send_notification, notify_about_new_post


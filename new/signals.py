from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings

from .models import PostCategory


def send_notification(preview, pk, title, subscribers):
    htlm_context = render_to_string(
        'email/post_created_email.html',
        {
            'text' : preview,
            'Link' : f'{settings.SITE_URL}/new/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject = title,
        body = '',
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = subscribers
    )

    msg.attach_alternative(htlm_context, 'text/html')
    msg.send()





@receiver(m2m_changed,sender = PostCategory)
def notify_about_new_post(sender,instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk, instance.title, subscribers)



from backend import settings
from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_collect_created(user_email):
    send_mail(
        'Групповой сбор',
        'Вы успешно создали групповой сбор!',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )


@shared_task
def send_donation_created(user_email):
    send_mail(
        'Платёж (донация)',
        'Вы успешно скинулись на групповой сбор!',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )

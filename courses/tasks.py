from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser
from datetime import datetime, timedelta
from pytz import timezone as tz


@shared_task
def _send_mail_course_update(recipient_list):
    send_mail(
        subject='Обновление курса',
        message=f'Обновление курса',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_list]
    )


@shared_task
def deactivate_users():
    users = CustomUser.objects.all()
    now = datetime.now().replace(tzinfo=tz('UTC'))
    deactivate_time = timedelta(days=120)
    for user in users:
        if user.last_login:
            if (now - user.last_login) > deactivate_time:
                user.is_active = False
                user.save()

from celery import shared_task
from django.core.mail import send_mail
import os
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model


@shared_task
def send_course_update_email(user_email, course_name, update_description):
    subject = f"Курс '{course_name}' обновлен!"
    message = f"Здравствуйте! В курсе '{course_name}' появились новые материалы: {update_description}"
    from_email = os.getenv('EMAIL_HOST_USER')
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    inactive_threshold = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=inactive_threshold, is_active=True)

    inactive_users.update(is_active=False)

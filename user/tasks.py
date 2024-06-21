from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_simple_email(body, subject, email, count):

    for i in range(count):
        print(i)
        email = f"{i}{email}"
        print(email)
        send_mail(subject, body, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[f"{email}"])
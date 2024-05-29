from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from celery import shared_task
from account.models import CustomUser

@shared_task
def send_verification_email(user_id):
    user = CustomUser.objects.get(id=user_id)
    token = user.generate_verification_token()

    subject = 'Verify Your Email'
    context = {
        'user': user,
        'verification_token': token,
    }
    html_message = render_to_string('verification_email.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

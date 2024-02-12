from .models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def is_user_active(username):
    user = CustomUser.objects.get(username=username)
    return user.is_active


def send_email_to_user(email, token):

    subject = 'Account Verification'
    message = f'Login with the token < {token} > to activate your account'

    context = {
        'subject': subject,
        'message': message
    }

    email_body = render_to_string('userAuth/email_templates.html', context)
    plaintext = strip_tags(email_body)
    send_mail(
            subject,
            plaintext,
            'maxwellodoom1729@gmail.com',
            [email],
            fail_silently=False,
        )





from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator  # instance of PasswordResetTokenGenerator
from django.core.mail import EmailMessage


def send_verification_email(request, user, mail_subject, email_template):
    message = render_to_string(email_template, context={
        'user': user,
        'protocol': request.scheme,
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()


def send_email_with_textmessage(request, user, mail_subject, text_message, email_template):
    message = render_to_string(email_template, context={
        'user': user,
        'text_message': text_message
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()

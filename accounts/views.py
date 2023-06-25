from django.shortcuts import render, redirect
from .forms import UserForm, UserEmailChangeForm
from .utils import send_verification_email, send_confirm_new_email, send_email_with_textmessage
from django.contrib import messages
from django.contrib import auth
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from datetime import timedelta
from django.http import HttpResponse
import logging


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            User = auth.get_user_model()
            user = User.objects.create_user(
                username=username, email=email,
                first_name=first_name, last_name=last_name,
                password=password
            )
            user.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/email/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered successfully.')
            return redirect('accounts:register_user')
        else:
            print('Invalid form')
            print(form.errors)
    else:
        if request.user.is_authenticated:
            return redirect('accounts:login')
        form = UserForm()
    context = {'form': form,}
    return render(request, 'accounts/register_user.html', context)


def user_activate(request, uid_b64, token):
    try:
        uid = urlsafe_base64_decode(uid_b64).decode()
        User = auth.get_user_model()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    except Exception:
        user = None
        logging.exception('user_activate error message:')
    if user is not None and default_token_generator.check_token(user, token):
        # default_token_generator.check_token checks if the timestamp is within limit defined by settings.PASSWORD_RESET_TIMEOUT
        user.is_active = True
        user.save()
        messages.success(request, 'High-Five! You have joined our service!')
        return redirect('accounts:activated')
    else:
        messages.error(request, 'Invalid activation link has been detected')
        return redirect('accounts:register_user')


def login(request):
    if request.user.is_authenticated:
        return HttpResponse('<h1>You have already logged in.</h1>')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)  # email has to be set up as USERNAME_FIELD at Custom User Model
        # authenticate() returns User object if exists
        if user is not None:
            auth.login(request, user)
            return HttpResponse('<h1>You have logged in successfully.</h1>')
        else:
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        User = auth.get_user_model()
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send email with reset password link
            mail_subject = 'Reset your password'
            email_template = 'accounts/email/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Your requesting account does not exist')
            return redirect('accounts:login')
    return render(request, 'accounts/forget_password.html')


def validate_reset_password(request, uid_b64, token):
    try:
        uid = urlsafe_base64_decode(uid_b64).decode()
        User = auth.get_user_model()
        user = User.objects.get(pk=uid)
    except Exception as e:
        logging.exception('validate_reset_password error message:')
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid  # To use uid in reset_password function
        return redirect('accounts:reset_password')
    else:
        return HttpResponse('This link has been expired.')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            User = auth.get_user_model()
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            del request.session['uid']
            mail_subject = 'New password has been set'
            email_template = 'accounts/email/reset_password_finish_email.html'
            text_message = 'New password has been set correctly.'
            send_email_with_textmessage(request, user, mail_subject, text_message, email_template)
            messages.success(request, 'New password has been set correctly.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Password does not match.')
            return redirect('accounts:reset_password')
    return render(request, 'accounts/reset_password.html')


@login_required(login_url='accounts:login')
def change_email(request):
    if request.method == 'POST':
        form = UserEmailChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            new_email = form.cleaned_data['email']

            mail_subject = 'Please confirm your new email'
            email_template = 'accounts/email/account_confirm_new_email.html'
            send_confirm_new_email(request, user, new_email, mail_subject, email_template)
            messages.success(request, 'Confirm new email link has been sent to your new email')
            return HttpResponse('<h1>Change email confirm link has been sent.</h1>')
    else:
        form = UserForm()
    context = {'form': form,}
    return render(request, 'accounts/change_email.html', context)


def change_email_confirm(request, uid_b64, token):
    try:
        uid = urlsafe_base64_decode(uid_b64).decode()
        User = auth.get_user_model()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    except Exception:
        user = None
        logging.exception('change_email_confirm error message:')

    # Check the token
    signer = signing.TimestampSigner(salt='django.core.signing')
    try:
        value_dict = signer.unsign_object(token, max_age=timedelta(days=1))
        new_email = value_dict['new_email']
        if user is not None:
            user.email = new_email
            user.save()
            return redirect('accounts:change_email_success')
    except Exception:
        logging.exception('change_email_confirm unsign error message:')
    return HttpResponse('This link has been expired.')

def change_email_success(request):
    return HttpResponse('<h1>Your email has been changed successfully.</h1>')


def activated(request):
    return HttpResponse('<h1>You have been activated!</h1>')

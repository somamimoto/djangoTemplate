from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import UserForm
from .utils import send_verification_email
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            User = get_user_model()
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
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register_user.html', context)


def user_activate(request, uid_b64, token):
    try:
        uid = urlsafe_base64_decode(uid_b64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # default_token_generator.check_token checks if the timestamp is within limit defined by settings.PASSWORD_RESET_TIMEOUT
        user.is_active = True
        user.save()
        messages.success(request, 'High-Five! You have joined our service!')
        return redirect('accounts:activated')
    else:
        messages.error(request, 'Invalid activation link has been detected')
        return redirect('accounts:register_user')


def activated(request):
    return HttpResponse('<h1>You have been activated!</h1>')

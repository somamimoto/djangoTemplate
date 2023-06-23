from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import UserForm
from .utils import send_verification_email
from django.contrib import messages


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(form.is_valid())
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
    pass

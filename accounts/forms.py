from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )

class UserEmailChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email',]

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email__exact=email, is_active=False).delete()
        return email

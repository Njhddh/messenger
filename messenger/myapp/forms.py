from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин или Email")


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Поле для ввода пароля

    class Meta:
        model = User
        fields = ['name', 'email', 'password']  # Поля, которые будут в форме

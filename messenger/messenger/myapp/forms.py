from .models import User
from django import forms
from .models import Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class NewDialogForm(forms.Form):
    email = forms.EmailField(label="Email пользователя")
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин или Email")


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

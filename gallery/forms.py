from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Форма авторизации"""
    username = forms.CharField(widget=forms.TextInput, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

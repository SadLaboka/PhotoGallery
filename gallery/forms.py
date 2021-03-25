from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Album, Category, Photo


class LoginForm(AuthenticationForm):
    """Форма авторизации"""
    username = forms.CharField(widget=forms.TextInput, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserRegisterForm(UserCreationForm):
    """Форма регистрации"""
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddAlbumForm(forms.ModelForm):
    """Форма добавления альбома"""
    title = forms.CharField(label='Название альбома', widget=forms.TextInput)
    image = forms.ImageField(label='Изображение для альбома', required=False)

    class Meta:
        model = Album
        fields = ('title', 'image')


class AddPhotoForm(forms.ModelForm):
    """Форма добавления фото"""

    class Meta:
        model = Photo
        fields = ('title', 'description', 'image', 'category', 'album', 'is_public')

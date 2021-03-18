from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.http import HttpResponseNotFound, HttpResponseRedirect

from .models import Photo, Category, Album
from .forms import LoginForm, UserRegisterForm, AddAlbumForm


class GalleryView(View):
    """Главная"""
    def get(self, request, *args, **kwargs):
        photos = Photo.objects.filter(is_public=True)
        categories = Category.objects.all()
        context = {'photos': photos, 'categories': categories}
        return render(request, 'gallery/gallery.html', context)


class PhotosByCategory(View):
    """Вывод фото по категориям"""
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        current_category = Category.objects.get(slug=kwargs['slug'])
        photos = Photo.objects.filter(category__slug=kwargs['slug'])
        context = {'categories': categories, 'photos': photos, 'current_category': current_category}
        return render(request, 'gallery/category_gallery.html', context)


class PhotosByAlbums(View):
    """Вывод фото из конкретного альбома"""
    def get(self, request, *args, **kwargs):
        current_album = Album.objects.get(pk=kwargs['pk'])
        if current_album.owner != request.user:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        photos = Photo.objects.filter(album__pk=kwargs['pk'])
        print(photos)
        context = {'current_album': current_album, 'photos': photos}
        return render(request, 'gallery/album_gallery.html', context)


class PhotoDetailView(View):
    """Детальный просмотр фото"""
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])
        if request.META.get('HTTP_REFERER'):
            previous_link = request.META['HTTP_REFERER']
        else:
            previous_link = r'/'
        context = {'photo': photo, 'previous': previous_link}
        return render(request, 'gallery/photo_detail.html', context)


class UserProfile(View):
    """Личная страница пользователя"""
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.filter(owner=request.user)
        context = {'photos': photo}
        return render(request, 'gallery/profile.html', context)


class UserAlbums(View):
    """Альбомы пользователя"""
    def get(self, request, *args, **kwargs):
        albums = Album.objects.filter(owner=request.user)
        context = {'albums': albums}
        return render(request, 'gallery/albums.html', context)


class CreateAlbum(View):
    """Создание альбома пользователя"""
    def get(self, request, *args, **kwargs):
        form = AddAlbumForm(request.POST or None)
        context = {'form': form}
        return render(request, 'gallery/add_album.html', context)

    def post(self, request, *args, **kwargs):
        form = AddAlbumForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.owner = request.user
            new_album.title = form.cleaned_data['title']
            new_album.image = form.cleaned_data['image']
            new_album.save()
            messages.success(request, 'Альбом успешно добавлен')
            return HttpResponseRedirect('/profile/albums/')
        else:
            messages.error(request, 'Ошибка добавления')
            context = {'form': form}
        return render(request, 'gallery/add_album.html', context)


class DeleteAlbum(View):
    """Удаление выбранного альбома"""
    def get(self, request, *args, **kwargs):
        album_pk = kwargs.get('pk')
        album = Album.objects.get(pk=album_pk)
        album.delete()
        messages.info(request, 'Альбом успешно удален')
        return HttpResponseRedirect('/profile/albums/')


def user_login(request):
    """Авторизирует пользователя"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'gallery/login.html', context={'form': form})


def user_logout(request):
    """Выходит"""
    logout(request)
    return redirect('home')


def register(request):
    """Регистирует пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'gallery/register.html', context={'form': form})

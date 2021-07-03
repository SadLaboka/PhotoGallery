from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.http import HttpResponseNotFound, HttpResponseRedirect

from .models import Photo, Category, Album
from .forms import LoginForm, UserRegisterForm, AddAlbumForm, AddPhotoForm


class GalleryView(View):
    """Главная"""
    def get(self, request, *args, **kwargs):
        photos = Photo.objects.filter(is_public=True).order_by('-pk')
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
        if request.user.is_authenticated:
            photo.views += 1
            photo.save()
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


class PhotoManagement(View):
    """Страница для управления фото"""
    def get(self, request, *args, **kwargs):
        photos = Photo.objects.filter(owner=request.user).order_by('-pk')
        context = {'photos': photos}
        return render(request, 'gallery/photo_management.html', context)


class AddPhoto(View):
    """Страница добавления фотографий"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = AddPhotoForm(request.POST or None)
            context = {'form': form}
            return render(request, 'gallery/add_photo.html', context)
        else:
            redirect('login')

    def post(self, request, *args, **kwargs):
        form = AddPhotoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.owner = request.user
            new_photo.title = form.cleaned_data['title']
            new_photo.description = form.cleaned_data['description']
            new_photo.image = form.cleaned_data['image']
            new_photo.category = form.cleaned_data['category']
            new_photo.album = form.cleaned_data['album']
            new_photo.is_public = form.cleaned_data['is_public']
            new_photo.save()
            messages.success(request, 'Фото успешно добавлено')
            return HttpResponseRedirect('/profile/photos/')
        else:
            messages.error(request, 'Ошибка добавления')
            context = {'form': form}
        return render(request, 'gallery/add_photo.html', context)


class EditPhoto(View):
    """Страница изменения фото"""
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])
        categories = Category.objects.all()
        albums = Album.objects.filter(owner=request.user)
        if request.META.get('HTTP_REFERER'):
            previous_link = request.META['HTTP_REFERER']
        else:
            previous_link = r'/'
        context = {'photo': photo, 'previous': previous_link, 'categories': categories, 'albums': albums}
        return render(request, 'gallery/edit_photo.html', context)

    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])
        data = request.POST
        print(data)
        photo.title = data['title']
        if data['category'] != 'none':
            photo.category = Category.objects.get(slug=data['category'])
        else:
            photo.category = None
        if data['album'] != 'none':
            photo.album = Album.objects.get(pk=data['album'])
        else:
            photo.album = None
        photo.description = data['description']
        if data.get('is_public'):
            photo.is_public = True
        else:
            photo.is_public = False
        photo.save(update_fields=['title', 'category', 'album', 'description', 'is_public'])
        return redirect('photo-management')


class DeletePhoto(View):
    """Удаление выбранного фото"""
    def get(self, request, *args, **kwargs):
        photo_pk = kwargs.get('pk')
        photo = Photo.objects.get(pk=photo_pk)
        photo.delete()
        messages.info(request, 'Фото успешно удалено')
        return HttpResponseRedirect('/profile/photos/')


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

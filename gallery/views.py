from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login

from .models import Photo, Category, Album
from .forms import LoginForm


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
        photos = Photo.objects.filter(category__slug=kwargs['slug'])
        context = {'categories': categories, 'photos': photos}
        return render(request, 'gallery/category_gallery.html', context)


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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'gallery/login.html', context={'form': form})

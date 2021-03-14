from django.shortcuts import render
from django.views import View

from .models import Photo, Category, Album


class GalleryView(View):

    def get(self, request, *args, **kwargs):
        photos = Photo.objects.filter(is_public=True)
        categories = Category.objects.all()
        context = {'photos': photos, 'categories': categories}
        return render(request, 'gallery/gallery.html', context)


class PhotosByCategory(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        photos = Photo.objects.filter(category__slug=kwargs['slug'])
        context = {'categories': categories, 'photos': photos}
        return render(request, 'gallery/category_gallery.html', context)


class PhotoDetailView(View):

    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])
        if request.META.get('HTTP_REFERER'):
            previous_link = request.META['HTTP_REFERER']
        else:
            previous_link = r'/'
        context = {'photo': photo, 'previous': previous_link}
        return render(request, 'gallery/photo_detail.html', context)

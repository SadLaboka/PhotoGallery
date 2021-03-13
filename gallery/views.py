from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import Photo, Category, Album


class GalleryView(View):

    def get(self, request, *args, **kwargs):
        photos = Photo.objects.filter(is_public=True)
        categories = Category.objects.all()
        context = {'photos': photos, 'categories': categories}
        return render(request, 'gallery/gallery.html', context)


class PhotoDetailView(DetailView):

    template_name = 'gallery/photo-detail.html'

from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView


class GalleryView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'gallery/gallery.html')


class PhotoDetailView(DetailView):

    template_name = 'gallery/photo-detail.html'

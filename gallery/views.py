from django.shortcuts import render
from django.views import View


class GalleryView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'gallery/gallery.html')

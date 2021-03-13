from django.urls import path

from .views import GalleryView, PhotoDetailView

urlpatterns = [
    path('', GalleryView.as_view(), name='home'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
]

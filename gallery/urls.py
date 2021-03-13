from django.urls import path

from .views import GalleryView, PhotoDetailView, PhotosByCategory

urlpatterns = [
    path('', GalleryView.as_view(), name='home'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('category/<str:slug>/', PhotosByCategory.as_view(), name='photos-by-category'),
]

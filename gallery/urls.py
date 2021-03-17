from django.urls import path

from .views import (
    GalleryView,
    PhotoDetailView,
    PhotosByCategory,
    UserProfile,
    UserAlbums,
    user_login,
    user_logout,
    register,
)

urlpatterns = [
    path('', GalleryView.as_view(), name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/albums/', UserAlbums.as_view(), name='albums'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('category/<str:slug>/', PhotosByCategory.as_view(), name='photos-by-category'),
]

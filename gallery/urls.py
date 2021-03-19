from django.urls import path

from .views import (
    GalleryView,
    PhotoDetailView,
    PhotosByCategory,
    PhotosByAlbums,
    PhotoManagement,
    DeletePhoto,
    UserProfile,
    UserAlbums,
    CreateAlbum,
    DeleteAlbum,
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
    path('profile/albums/add/', CreateAlbum.as_view(), name='add-album'),
    path('profile/albums/delete/<int:pk>', DeleteAlbum.as_view(), name='delete-album'),
    path('profile/albums/<int:pk>/', PhotosByAlbums.as_view(), name='photos-by-album'),
    path('profile/photos/', PhotoManagement.as_view(), name='photo-management'),
    path('profile/photos/delete/<int:pk>', DeletePhoto.as_view(), name='delete-photo'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('category/<str:slug>/', PhotosByCategory.as_view(), name='photos-by-category'),
]

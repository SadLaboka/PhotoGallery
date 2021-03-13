from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Категории фотографий"""
    title = models.CharField(max_length=50, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Album(models.Model):
    """Альбомы для фотографий"""
    title = models.CharField(max_length=100, verbose_name='Название')
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Photo(models.Model):
    """Фотографии"""
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(verbose_name='Фото')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(verbose_name='Публичность', default=False)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    """Общие категории фотографий"""
    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='Url', max_length=100, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photos-by-category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Album(models.Model):
    """Пользовательские альбомы для фотографий"""
    title = models.CharField(max_length=100, verbose_name='Название')
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to='Albums/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Photo(models.Model):
    """Фотографии"""
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(verbose_name='Фото', upload_to='Photo/%Y/%m/%d/')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='photos'
    )
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(verbose_name='Публичность', default=False)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})

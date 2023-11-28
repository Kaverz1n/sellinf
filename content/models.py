from django.db import models

from users.models import User


class Content(models.Model):
    '''
    Content model class
    '''
    TYPE_CHOICES = (
        ('premium', 'Premium'),
        ('free', 'Free'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='owner')
    title = models.CharField(max_length=100, verbose_name='title', unique=True)
    content = models.TextField(verbose_name='content')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, verbose_name='type')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
    views = models.IntegerField(default=0, verbose_name='views')
    is_published = models.BooleanField(default=False, verbose_name='published')

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = 'content'
        verbose_name_plural = 'contents'

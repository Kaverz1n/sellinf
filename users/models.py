from django.contrib.auth.models import AbstractUser
from django.db import models

from PIL import Image

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    '''
    User model
    '''
    username = None
    phone = models.CharField(max_length=15, unique=True, verbose_name='phone')
    nickname = models.CharField(max_length=30, unique=True, verbose_name='nickname')
    about = models.TextField(max_length=850, verbose_name='about', **NULLABLE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', verbose_name='image')
    is_upgraded = models.BooleanField(default=False, verbose_name='is_upgraded')
    subscribers = models.IntegerField(default=0, verbose_name='subscribers')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone}'

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        max_size = (300, 300)

        # resize image if it is bigger than max_size
        if img.size != max_size:
            resized_image = img.resize(max_size)
            resized_image.save(self.image.path)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class ConfirmationCode(models.Model):
    '''
    Confirm code model
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name='user')
    code = models.IntegerField(unique=True, verbose_name='code')

    def str_code(self) -> str:
        return f'{self.user.phone} - {self.code}'

    class Meta:
        verbose_name = 'confirmation code'
        verbose_name_plural = 'confirmation codes'

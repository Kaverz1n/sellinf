from django.db import models

from users.models import User


class Payment(models.Model):
    '''
    Payment model
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    date = models.DateTimeField(auto_now_add=True, verbose_name='date')
    checkout_id = models.CharField(max_length=255, verbose_name='checkout id', unique=True)

    def __str__(self) -> str:
        return f'Payment {self.user.phone}'

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payment'

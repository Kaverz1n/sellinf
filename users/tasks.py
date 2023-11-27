from celery import shared_task
from sendsms import api

from users.models import ConfirmationCode


@shared_task
def send_confirmation_code(phone: str) -> None:
    '''
    Send confirmation code to phone
    '''
    code = ConfirmationCode.objects.get(user__phone=phone).code

    api.send_sms(
        body=f'Your confirmation code is: {code}',
        from_phone='+9999',
        to=[f'{phone}']
    )
import django

import random

from users.models import ConfirmationCode, User
from users.tasks import send_confirmation_code


def code_generation(user: User) -> None:
    '''
    Create a confirmation code
    '''
    code = int(''.join([str(random.randint(1, 9)) for _ in range(4)]))

    try:
        ConfirmationCode.objects.create(user=user, code=code)
    except django.db.utils.IntegrityError:
        users_code = ConfirmationCode.objects.get(user=user)
        users_code.code = code
        users_code.save()

    send_confirmation_code.delay(user.phone)

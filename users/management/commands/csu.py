from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    '''
    The command to create a superuser
    '''

    def handle(self, *args, **options) -> None:
        try:
            user = User.objects.create(
                phone='+9',
                nickname='Admin',
                is_upgraded=True,
                is_staff=True,
                is_superuser=True,
            )

            user.set_password('Admin')
            user.save()

            self.stdout.write('Superuser created successfully')
        except Exception as e:
            self.stderr.write(f'Error creating superuser: {e}')

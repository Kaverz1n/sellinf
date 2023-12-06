from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    '''
    Command to load data from database json file.
    '''

    def handle(self, *args, **options) -> None:
        try:
            ContentType.objects.all().delete()
            call_command('loaddata', 'database_data.json')
        except:
            self.stderr.write('Error loading database data')

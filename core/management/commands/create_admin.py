from django.core.management.base import BaseCommand
from core.models import CustomUser

class Command(BaseCommand):
    help = 'Create superuser for phone-based auth'

    def handle(self, *args, **kwargs):
        phone    = '9999999999'
        name     = 'Admin'
        password = 'Admin@1234'

        if CustomUser.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists. Skipping.'))
            return

        CustomUser.objects.create_superuser(phone=phone, name=name, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser created: {phone}'))
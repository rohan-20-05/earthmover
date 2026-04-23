from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from core.models import CustomUser


class Command(BaseCommand):
    help = 'Fresh superuser creation'

    def handle(self, *args, **kwargs):
        # Step 1: Wipe everything
        CustomUser.objects.all().delete()
        self.stdout.write('All users deleted.')

        # Step 2: Create fresh superuser manually
        user = CustomUser(
            phone='9167164491',
            name='Admin',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        user.password = make_password('Admin@1234')
        user.save()

        self.stdout.write(f'Created: {user.phone}')
        self.stdout.write(f'is_active: {user.is_active}')
        self.stdout.write(f'is_staff: {user.is_staff}')
        self.stdout.write(f'is_superuser: {user.is_superuser}')
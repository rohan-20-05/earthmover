from django.core.management.base import BaseCommand
from core.models import CustomUser


class Command(BaseCommand):
    help = 'Force create superuser'

    def handle(self, *args, **kwargs):
        phone    = '9167164491'
        name     = 'Admin'
        password = 'Admin@1234'

        # Delete all existing superusers
        CustomUser.objects.filter(is_superuser=True).delete()
        self.stdout.write(self.style.WARNING('Deleted old superusers.'))

        # Create fresh one
        user = CustomUser.objects.create_superuser(
            phone=phone,
            name=name,
            password=password
        )

        # Force all flags to be correct
        user.is_active    = True
        user.is_staff     = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Superuser created: {user.phone}'))
        self.stdout.write(self.style.SUCCESS(f'is_active={user.is_active}'))
        self.stdout.write(self.style.SUCCESS(f'is_staff={user.is_staff}'))
        self.stdout.write(self.style.SUCCESS(f'is_superuser={user.is_superuser}'))
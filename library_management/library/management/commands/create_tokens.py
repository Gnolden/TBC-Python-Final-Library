# management/commands/create_tokens.py
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from library.models import User

class Command(BaseCommand):
    help = 'Create tokens for all users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created token for user: {user.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Token already exists for user: {user.username}'))

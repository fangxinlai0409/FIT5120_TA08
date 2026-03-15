from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    # This script triggers Django's internal PBKDF2 hashing for MySQL storage
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('--admin', action='store_true')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        is_admin = options['admin']

        try:
            if is_admin:
                User.objects.create_superuser(username=username, password=password, email='')
                role = "Superuser"
            else:
                User.objects.create_user(username=username, password=password)
                role = "Standard User"

            self.stdout.write(self.style.SUCCESS(f'Successfully created {role}: {username}'))

        except IntegrityError:
            raise CommandError(f'User "{username}" already exists.')
        except Exception as e:
            raise CommandError(f'Error: {e}')
        






# Django User Utility

#This project includes a custom CLI tool to securely populate your MySQL database with users.

# How to add this to your Backend
#1. Ensure your Django app is listed in `INSTALLED_APPS` in `settings.py`.
#2. Create the folder structure: `your_app/management/commands/`.
#3. Place `create_app_user.py` in that folder.
#4. Django will automatically detect the command.


## Usage
#Run these commands from your terminal (M2 Mac use `python3`):


### Create a Regular User
#```bash
#python3 manage.py create_app_user my_username my_password



####Technical Security
#Hashing: Uses Django's default PBKDF2 with SHA-256.

#MySQL Compatibility: Automatically handles table insertion into the auth_user table.

#Zero Plaintext: Passwords are hashed in memory before being sent to MySQL.
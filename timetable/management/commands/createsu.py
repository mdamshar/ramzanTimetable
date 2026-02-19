from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username="amshar").exists():
            User.objects.create_superuser("amshar", "amsharjlk@gmail.com", "jlk@#0541")
            self.stdout.write("Superuser created.")
        else:
            self.stdout.write("Superuser already exists.")

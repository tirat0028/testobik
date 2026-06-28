import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dds_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Суперпользователь создан:\nЛогин: {username}\nПароль: {password}")
else:
    print("Суперпользователь уже существует")

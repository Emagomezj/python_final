from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os

def get_random_filename(instance, filename):
    ext = filename.split('.')[-1]
    folder = 'avatares'
    return os.path.join(folder, f'file.{uuid.uuid4().hex}.{ext}')

# Create your models here.
class App_Users(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
class Avatar(models.Model):
    user = models.OneToOneField(App_Users, on_delete=models.CASCADE, related_name='avatar')
    image = models.ImageField(upload_to=get_random_filename, blank=True, null=True, default='avatares/default_avatar.svg')
    def __str__(self):
        return f'{self.user} - {self.image}'
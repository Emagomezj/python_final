from django.db import models
from users.models import App_Users
import uuid
import os

def get_random_filename(instance, filename):
    ext = filename.split('.')[-1]
    folder = 'blogs_imgs'
    return os.path.join(folder, f'file.{uuid.uuid4().hex}.{ext}')

# Create your models here.
class Blogs(models.Model):
    author = models.ForeignKey(App_Users, null=True, on_delete=models.SET_NULL, related_name='blogs')
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def day_with_leading_zero(self):
        return str(self.created_at.strftime("%d"))

    @property
    def month_with_leading_zero(self):
        return str(self.created_at.strftime("%m"))
    def __str__(self):
        return f'{self.title}'
    @property
    def post_count(self):
        return self.post_set.count()

class Blog_img(models.Model):
    blog = models.OneToOneField(Blogs, on_delete=models.CASCADE, related_name='thumbnail')
    image = models.ImageField(upload_to=get_random_filename, blank=True, null=True, default='blogs_imgs/default_blog_img.jpg')
    def __str__(self):
        return f'{self.blog.title} - {self.image}'
    
class Post(models.Model):
    author = models.ForeignKey(App_Users,null=True, on_delete=models.SET_NULL, related_name='posts')
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Post de {self.author} en {self.blog}'
    
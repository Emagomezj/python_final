from django.db import models
from users.models import App_Users

# Create your models here.
class Blogs(models.Model):
    author = models.ForeignKey(App_Users, null=True, on_delete=models.SET_NULL, related_name='blogs')
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.title}'
    
class Post(models.Model):
    author = models.ForeignKey(App_Users,null=True, on_delete=models.SET_NULL, related_name='posts')
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Post de {self.author} en {self.blog}'
    
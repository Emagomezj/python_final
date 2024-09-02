from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import App_Users
from .models import Blogs, Post

class BlogForm(forms.ModelForm):
    title = forms.TextInput()
    keywords = forms.CharField(max_length=100)
    description = forms.Textarea()
    thumbnail = forms.ImageField(required=False)
    class Meta:
        model = Blogs
        fields = ['title', 'keywords', 'description','thumbnail']

class PostForm(forms.ModelForm):
    content= forms.Textarea()
    class Meta:
        model = Post
        fields = ['author', 'blog', 'content']
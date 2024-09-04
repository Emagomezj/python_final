from django import forms
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
        fields = ['content']

class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=100)

        

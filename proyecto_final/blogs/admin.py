from django.contrib import admin
from .models import Blogs, Blog_img, Post

@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'description', 'keywords')
    list_filter = ('created_at', 'author')

@admin.register(Blog_img)
class BlogImgAdmin(admin.ModelAdmin):
    list_display = ('blog', 'image')
    search_fields = ('blog__title',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at', 'author', 'blog')
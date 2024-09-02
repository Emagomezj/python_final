from django.urls import path
from blogs import views
from .views import (
    BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView,
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,show_default_image_url
)

urlpatterns = [
    path('', BlogListView.as_view(), name = 'Home'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/new/', BlogCreateView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_update'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('default-image-url/', show_default_image_url, name='default_image_url'),
    path('about_us', views.about_us, name='About_us')
    # path('/blog/<bid>',)
]
from django.urls import path
from blogs import views

urlpatterns = [
    path('', views.home, name = 'Home')
]
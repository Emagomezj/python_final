from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register', views.register, name="Register"),
    path('login',views.login_request, name="Login"),
    path('edit', views.editar_perfil,name='Edit_User'),
    path('logout',LogoutView.as_view(template_name='users/logout.html'), name= 'Logout'),
    path('change_pass', views.CambiarPass.as_view(), name="ChangePass")
]
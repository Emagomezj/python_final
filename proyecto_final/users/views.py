from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from users.forms import UserEditForm, UserRegisterForm
from users.models import Avatar
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

def login_request(request):
    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            pwrd = form.cleaned_data.get('password')
            
            user = authenticate(username= usuario, password=pwrd)

            
            if user is not None:
                login(request, user)
                return redirect('Home')

        msg_login = "Usuario o contraseña incorrectos"

    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "msg_login": msg_login})

def register(request):
    msg_register = ""
    if request.method == 'POST':

        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'image' in request.FILES:
                
                Avatar.objects.create(user=user,image=request.FILES['image'])
            else:
                
                Avatar.objects.create(user=user)
            return redirect("Home")
        else:
            msg_register = "Error en los datos ingresados"
            msg_register += f" | {form.errors}"

    form = UserRegisterForm()     
    return render(request,"users/registro.html" ,  {"form":form, "msg_register": msg_register})

# Vista de editar el perfil
# Obligamos a loguearse para editar los datos del usuario
@login_required
def editar_perfil(request):
    # El usuario para poder editar su perfil primero debe estar logueado.
    # Al estar logueado, podremos encontrar dentro del request la instancia
    # del usuario -> request.user
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=usuario)
        if miFormulario.is_valid():
            
            if miFormulario.cleaned_data.get('image'):
                usuario.avatar.image = miFormulario.cleaned_data.get('image')
                usuario.avatar.save()
            miFormulario.save()

            return redirect("Home")

    else:
        miFormulario = UserEditForm(instance=usuario)

    return render(request, "users/edit_user.html", {"mi_form": miFormulario, "usuario": usuario})


class CambiarPass(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/edit_pass.html"
    success_url = reverse_lazy("Edit_User")
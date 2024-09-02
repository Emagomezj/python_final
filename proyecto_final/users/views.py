from django.shortcuts import render, redirect

from django.core.exceptions import PermissionDenied
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.core.files.storage import default_storage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from users.forms import UserEditForm, UserRegisterForm
from users.models import Avatar
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from users.models import App_Users

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
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=usuario)
        if miFormulario.is_valid():
            usuario = miFormulario.save(commit=False)

            # Verifica si hay una imagen en request.FILES
            if 'image' in request.FILES:
                # Eliminar la imagen antigua si existe
                if usuario.avatar and usuario.avatar.image.name != 'avatars/default_avatar.jpg':
                    old_image = usuario.avatar.image
                    if default_storage.exists(old_image.name):
                        default_storage.delete(old_image.name)
                
                # Actualizar la imagen nueva
                if usuario.avatar:
                    usuario.avatar.image = request.FILES['image']
                    usuario.avatar.save()
                else:
                    Avatar.objects.create(user=usuario, image=request.FILES['image'])
            
            usuario.save()
            return redirect("Home")
    else:
        miFormulario = UserEditForm(instance=usuario)

    return render(request, "users/edit_user.html", {"mi_form": miFormulario, "usuario": usuario})

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = App_Users
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('Home')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.get_object()
        if hasattr(user, 'avatar') and user.avatar.image and user.avatar.image.name != 'blogs_imgs/default_blog_img.jpg':
            old_image = user.avatar.image
            if default_storage.exists(old_image.name):
                default_storage.delete(old_image.name)

        logout(self.request)
        
        return super().form_valid(form)

class CambiarPass(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/edit_pass.html"
    success_url = reverse_lazy("Edit_User")
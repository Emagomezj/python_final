from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import App_Users

class UserEditForm(UserChangeForm):
    password = None
    email = forms.EmailField(label="Ingrese su email")
    last_name = forms.CharField(label="Apellido", required=False)
    first_name = forms.CharField(label="Nombre", required=False)
    image = forms.ImageField(required=False)
    description = forms.Textarea()

    class Meta:
        model = App_Users
        fields = ['email', 'last_name', 'first_name', 'image', 'description']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Username")
    email = forms.EmailField()
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)
    description = forms.Textarea()
    image = forms.ImageField(required=False)

    class Meta:
        model = App_Users
        fields = ["username", "email", "password1", "password2", 'description', 'image', 'first_name', "last_name"]
        # Si queremos EDIAR los mensajes de ayuda editamos este dict,
            # de lo contrario lo limpiamos de ésta forma.
        #help_text = {k: "" for k in fields}
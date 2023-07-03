from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Avatar


class PostFormulario(forms.Form):

    title = forms.CharField()
    intro = forms.CharField()
    body = forms.CharField()
    post_image = forms.ImageField()


class MyUserCreationForm(UserCreationForm):

    username = forms.CharField(label='User Name', widget=forms.TextInput)
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat your Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k: '' for k in fields}


class UserEditForm(forms.Form):
    # agrego opciones a Editar en el Perfil de Usuario
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='EMail')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat your Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {k: '' for k in fields}

class AvatarFormulario(forms.ModelForm):
    user_image = forms.ImageField(label="imagen")
   

class AvatarFormulario(forms.Form):
    user_image = forms.ImageField(label="imagen")
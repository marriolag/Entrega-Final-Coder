from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Post
from .forms import *

# Create your views here.


def base(request):
    return render(request, 'blog/base.html')


def homepage(request):
    posts = Post.objects.all()
    return render(request, 'blog/homepage.html', {'posts': posts})


def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def create_post(request):

    if request.method == 'POST':
        miFormulario = PostFormulario(request.POST, request.FILES)
        print(miFormulario)

        if miFormulario.is_valid:
            informacion = miFormulario.cleaned_data
            publicacion = Post(title=informacion['title'], intro=informacion['intro'],
                               body=informacion['body'], post_image=informacion['post_image'])
            publicacion.save()
            return render(request, 'blog/homepage.html')

    else:
        miFormulario = PostFormulario()

    return render(request, 'blog/create_post.html', {"miFormulario": miFormulario})


@login_required
def erase_post(request, id):
    post_erased = Post.objects.get(id=id)
    post_erased.delete()

    # direcciono a pagina donde indico el Post que se borra
    return render(request, 'blog/erase_post.html', {'post': post_erased})


@login_required
def edit_post(request, post_id):
    # recibo el nombre del post que voy a modificar
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        # recibo la informacion del HTML (lo que ingresa el usuario)
        miPost = PostFormulario(request.POST)
        print(miPost)

        # si pasa la validacion de Django (CharField,TextField, length, etc)
        if miPost.is_valid:
            # el 'cleaned_data' va a limpiar la data que trae el formulario
            infopost = miPost.cleaned_data

            # aca voy a definir los campos que quiero o permito editar
            post.title = infopost['title']
            post.intro = infopost['intro']
            post.body = infopost['body']

            # con el save() se graba la info nuevamente en post, con el 'id' que di al principio
            post.save()

            # Back to HomePage
            return render(request, 'blog/homepage.html')

    else:

        miPost = PostFormulario(
            initial={'title': post.title, 'intro': post.intro, 'body': post.body})

    return render(request, 'blog/edit_post.html', {'miPost': miPost, 'post_id': post_id})


def login_request(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.cleaned_data.get('username')
            psw = form.cleaned_data.get('password')

            user = authenticate(username=user, password=psw)

            if user is not None:
                login(request, user)
                contexto = {'mensaje': f'Welcome {user}'}
                return render(request, 'blog/homepage.html', contexto)
            else:
                return render(request, 'blog/login.html', {'mensaje': 'Error: User not existing', 'form': form})

        else:
            contexto = {
                'mensaje': 'Error: User or Password Incorrect', 'form': form}
            return render(request, 'blog/login.html', contexto)

    contexto = {'form': form}
    return render(request, 'blog/login.html', contexto)


def register(request):

    if request.method == 'POST':
        #  form = UserCreationForm(request.POST)
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            contexto = {'mensaje': 'User created successfully!'}
            return render(request, 'blog/homepage.html', contexto)

    # si el usuario aun no se ha registrado, con el else le damos un formulario vacio
    else:
        # form = UserCreationForm()
        form = MyUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


class PostList(ListView):
    model = Post
    template_name = 'blog/homepage.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class CreatePost(CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('base')
    fields = ['title', 'intro', 'body']


class PostUpdate(UpdateView):
    model = Post
    template_name = 'blog/edit_post.html'
    success_url = reverse_lazy('base')
    fields = ['title', 'intro', 'body']


class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/erase_post.html'
    success_url = reverse_lazy('base')


@login_required
def edit_profile(request):
    usuario = User.objects.get(username=request.user)

    if request.method == 'POST':
        mi_form = UserEditForm(request.POST)

        if mi_form.is_valid():
            info = mi_form.cleaned_data

            usuario.username = info['username']
            usuario.email = info['email']
            usuario.last_name = info['last_name']
            usuario.first_name = info['first_name']

            usuario.save()

            return redirect('/blog')

    else:
        mi_form = UserEditForm(initial={'username': usuario.username,
                                        'email': usuario.email, 'last_name': usuario.last_name, 'first_name': usuario.first_name})

    return render(request, 'blog/edit_profile.html', {'mi_form': mi_form})


@login_required
def add_avatar(request):
    if request.method == 'POST':
        mi_form = AvatarFormulario(request.POST, request.FILES)
        if mi_form.is_valid():
            avatar_anterior = Avatar.objects.filter(user=request.user)
            if (len(avatar_anterior) > 0):
                avatar_anterior.delete()
            avatar_nuevo = Avatar(user=request.user, user_image=mi_form.cleaned_data["user_image"])
            avatar_nuevo.save()
            return render(request, 'blog/homepage.html')

    else:
        mi_form = AvatarFormulario()

    return render(request, 'blog/add_avatar.html', {'mi_form': mi_form})
    
def about_me(request):
    return render(request, 'blog/aboutme.html')


def page_notfound(request, exception):
    return render(request, 'blog/notfound.html')
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('homepage/', homepage, name='homepage'),
    path('post/<id>/', post_detail, name='post_detail'),
    path('create-post/', create_post, name='create_post'),
    path('erase-post/<id>/', erase_post, name='erase_post'),
    path('edit-post/<post_id>/', edit_post, name='edit_post'),
    path('login/', login_request, name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('add-avatar/', add_avatar, name='add-avatar'),
    path('about-me/', about_me, name='about-me')
]
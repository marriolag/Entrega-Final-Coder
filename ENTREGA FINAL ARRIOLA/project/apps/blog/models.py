from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=300)
    intro = models.TextField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to='PostImages', null=True, blank=True)


    class Meta:
        ordering = ['-date_added']

class Avatar(models.Model):
    # vinculo con el perfil de usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # subcarpeta avatares
    user_image = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
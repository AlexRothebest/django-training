from django.db import models
from django.contrib.auth.models import User as AuthUser


class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)


    def __str__(self):
        return self.name + ' ' + self.surname

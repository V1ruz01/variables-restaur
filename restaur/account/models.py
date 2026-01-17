from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserModel(models.Model):
    nickname = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.nickname
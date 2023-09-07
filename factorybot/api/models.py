from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['name']
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100, blank=True)
    chat_id = models.CharField(max_length=100, blank=True)


class Message(models.Model):
    date = models.DateField(auto_now=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User


class register(models.Model):
    name=models.CharField(max_length=100)
    
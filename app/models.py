from django.db import models
from account.models import User


class Blog(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)

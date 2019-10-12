
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
import collections

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    address = models.CharField(blank=True , max_length=255 , default='')
    phone =models.BigIntegerField(default=1234567890)
    isadmin = models.CharField(blank=True, max_length=255,default="User")

    def __str__(self):
        return self.email


class Articles(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    author = models.CharField(max_length=100, blank=True, default='')
    language = models.CharField( max_length=100)

    class Meta:
        ordering = ('created',)

class ArticleHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="article")

    class Meta:
        ordering = ('created',)

class Bookmark(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    date_created = models.DateTimeField(blank = True ,null=True,default = datetime.now())
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_bookmark")

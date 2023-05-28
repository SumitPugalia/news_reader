from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.urls import reverse
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "tags"

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=10000)
    posted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="tags")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    viewed = models.IntegerField(default=0)

    class Meta:
        db_table = "posts"

class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscriber_id", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "subscriptions"

from os import name
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
# Create your models here.


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=13, default="")
    email = models.EmailField(max_length=255, default="")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, default="", null=True, blank=True)
    organisation = models.CharField(max_length=300, default="", null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True, default="")
    display_pic = ResizedImageField(size=[400, 400], crop=['middle', 'center'],quality=100, upload_to="pic_folder", blank=True, null=True)
    website = models.CharField(max_length=255, null=True, blank=True, default="")
    facebook = models.CharField(max_length=255, null=True, blank=True, default="")
    instagram = models.CharField(max_length=255, null=True, blank=True, default="")
    twitter = models.CharField(max_length=255, null=True, blank=True, default="")
    github = models.CharField(max_length=255, null=True, blank=True, default="")


    def __str__(self):
        return str(self.user)

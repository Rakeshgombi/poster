from os import name
from django.db import models
from django.contrib.auth.models import User

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
  bio = models.TextField()
  organisation = models.CharField(max_length=300, default="")
  country = models.CharField(max_length=50, default="")
  display_pic = models.FileField(upload_to="pic_folder")
  website = models.CharField(max_length=255, null=True, blank=True, default="")
  facebook = models.CharField(max_length=255, null=True, blank=True, default="")
  instagram = models.CharField(max_length=255, null=True, blank=True, default="")
  twitter = models.CharField(max_length=255, null=True, blank=True, default="")
  github = models.CharField(max_length=255, null=True, blank=True, default="")

  def __str__(self):
      return str(self.user)
from django.db import models
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
# Create your models here.


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, default="")
    title = models.CharField(max_length=300, default="")
    author = models.CharField(max_length=255, default="")
    content = RichTextField(blank=True, null=True)
    thumbnail = ResizedImageField(size=[300, 600], crop=['middle', 'center'], quality=100, upload_to="blogThumbs", blank=True, null=True)
    # content = models.TextField()
    slug = models.CharField(max_length=350)
    views = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (by {self.author})"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # manually deactivate inappropriate comments from admin site
    active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/post/%i/" % self.id

class Project(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    download = models.CharField(max_length=300)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class Monkey(models.Model):
    bananas = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    def __str__(self):
        return self.field_name


class Comment(models.Model):
    name = models.CharField(max_length = 25)
    comment = models.TextField()
    date_added = models.DateTimeField(default = timezone.now)
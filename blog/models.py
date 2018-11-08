from os import path
from random import randint

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from blog_website.utils import unique_slug_generator


def get_filename_ext(filename):
    filepath = path.basename(filename)
    name, ext = path.splitext(filepath)
    return name, ext

def upload_name_path(instance, filename):
    folderName = randint(1, 40000000)
    filenam = randint(1, folderName)
    name, ext = get_filename_ext(filename)
    return f'products/{folderName}/{filenam}{ext}'

class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-updated')
    def get_published(self):
        return super().get_queryset().filter(publish=True).order_by('-updated')

class Post(models.Model):
    title       = models.CharField(max_length=250)
    slug        = models.SlugField(blank=True, null=True)
    thumbnail   = models.ImageField(upload_to = upload_name_path, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    publish     = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})

def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(post_pre_save_receiver, sender = Post)

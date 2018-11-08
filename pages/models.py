from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from blog_website.utils import unique_slug_generator


class PageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-updated')
    def get_published(self):
        return super().get_queryset().filter(publish=True).order_by('-updated')

class Page(models.Model):
    title        = models.CharField(max_length=50)
    slug        = models.SlugField(blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    Content     = RichTextUploadingField()
    publish     = models.BooleanField(default=False)

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"

    objects = PageManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages_detail", kwargs={"slug": self.slug})

def page_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(page_pre_save_receiver, sender = Page)
from django.contrib import admin
from .models import Post

class adminpost(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['timestamp', 'updated']

admin.site.register(Post, adminpost)
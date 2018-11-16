from django.conf import settings
from django.shortcuts import (Http404, HttpResponse, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.http import require_POST

from pages.models import Page

from .forms import SearchForm
from .models import Post


def post_list_view(request):
    """Home page View

This is the view which renders the home page of blog"""
    searchform = SearchForm()
    qs = Post.objects.get_published()
    if request.GET.get('s') != None:
        qs = Post.objects.get_published().filter(title__icontains=request.GET['s'])    
    pages = Page.objects.get_published()
    posts = Post.objects.get_published()[0:6]
    context = {
        'search'    : searchform,
        'qs'        : qs,
        'title'     : settings.SITE_TITLE,
        'pages'     : pages,
        'posts'     : posts,
    }
    return render(request, 'post_list.html', context)
    
def post_detail_view(request, slug):
    pages = Page.objects.get_published()
    searchform = SearchForm()
    if request.user.is_superuser:
        post_object = get_object_or_404(Post, slug=slug)
    else:
        post_object = get_object_or_404(Post, slug=slug, publish=True)
    posts = Post.objects.get_published()[0:6]
    context={
        'posts'     : posts,
        'search'    : searchform,
        'pages'     : pages,
        'post'      : post_object,
        'title'     : settings.SITE_TITLE,
    }
    return render(request, 'post.html', context)

@require_POST
def post_search_handler(request):
    searchform = SearchForm(request.POST or None)
    if searchform.is_valid:
        return redirect(reverse('list') + '?s=' + request.POST['search'])

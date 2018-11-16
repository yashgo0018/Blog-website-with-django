from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import Page
from .forms import ContactForm

from blog.models import Post
from blog.forms import SearchForm

common_context = {
    'search'    : SearchForm(),
    'title'     : settings.SITE_TITLE,
}

def page_detail_view(request, slug):
    page = get_object_or_404(Page, slug=slug, publish=True)
    pages = Page.objects.get_queryset()
    posts = Post.objects.get_published()[0:6]
    context = {
        'posts'     : posts,
        'pages'     : pages,
        'page'      : page,
    }
    context.update(common_context)
    return render(request, 'page.html', context)

def contact_page_view(request):
    contactform = ContactForm()
    pages = Page.objects.get_queryset()
    posts = Post.objects.get_published()[0:6]
    context = {
        'posts'     : posts,
        'pages'     : pages,
        'form'      : contactform,
    }
    context.update(common_context)
    return render(request, 'contact.html', context)
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from blog.forms import SearchForm
from blog.models import Post
from pages.models import Page

from .forms import (PageForm, PostForm, RegisterForm, SubscriberLoginForm,
                    UserForm, UserUpdateForm, LoginForm)

#common context
common = {
    'title'     : settings.SITE_TITLE,
}

def logout_page(request):
    logout(request)
    return redirect('login')

def subscriber_login_page(request):
    if request.user.is_authenticated:
        return redirect('subscriber_logout_page')
    searchform = SearchForm()
    form = SubscriberLoginForm(request.POST or None)
    posts = Post.objects.get_published()[0:6]
    context={
        'posts'     : posts,
        'page_title': 'Login',
        'form'      : form,
        'search'    : searchform,
        'pages'     : Page.objects.get_published(),
    }
    if form.is_valid():
        username = form.cleaned_data["UserName"]
        password = form.cleaned_data["PassWord"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            context['error'] = 'Username and Password Doesn\'t match!!!'
            context['form'] = SubscriberLoginForm()
    context.update(common)
    return render(request, 'auth.html', context)

def subscriber_logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('subscriber_login_page')
    else:
        searchform = SearchForm()
        posts = Post.objects.get_published()[0:6]
        context={
            'posts'     : posts,
            'pages'   :Page.objects.get_published(),
            'search'    : searchform,
        }
        context.update(common)
        return render(request, 'logout.html', context)

def subscriber_register_page(request):
    if request.user.is_authenticated:
        return redirect('subscriber_logout_page')
    form = RegisterForm(request.POST or None)
    searchform = SearchForm()
    posts = Post.objects.get_published()[0:6]
    context={
        'form'      : form,
        'page_title': 'Register',
        'posts'     : posts,
        'search'    : searchform,
        'pages'   :Page.objects.get_published(),
    }
    if form.is_valid():
        username = form.cleaned_data["UserName"]
        password = form.cleaned_data["PassWord"]
        firstname = form.cleaned_data["FirstName"]
        lastname = form.cleaned_data["LastName"]
        email = form.cleaned_data["Email"]
        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.save()
        return redirect('subscriber_login_page')
    context.update(common)
    return render(request, 'auth.html', context)

def login_page(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    context={
        'form'      : form,
        'user_count': User.objects.all().count(),
        'post_count': Post.objects.all().count(),
        'page_count': Page.objects.all().count(),
    }
    if form.is_valid():
        username = form.cleaned_data["UserName"]
        password = form.cleaned_data["PassWord"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('dashboard')
            else:
                logout(request)
                context['error'] = 'Permission Denied!!!'
        else:
            context['error'] = 'Username and Password Doesn\'t match!!!'
            context['form'] = LoginForm()
    context.update(common)
    return render(request, 'accounts/login.html', context)

def dashboard(request):
    if not check(request):
        return redirect('login')
    qs = User.objects.all()[::-1][0:5]
    context={
        'qs': qs,
        'user_count': User.objects.all().count(),
        'post_count': Post.objects.all().count(),
        'page_count': Page.objects.all().count(),
    }
    context.update(common)
    return render(request, 'accounts/index.html', context)

def list_content(request):
    if not check(request):
        return redirect('login')
    #checking the url
    url_string          = request.path.split('/')[2]
    is_page             = url_string == 'pages'
    is_post             = url_string == 'posts'
    is_user             = url_string == 'users'
    is_password    = request.path == reverse('passwords')

    #declaring the model and modelform
    if is_page:
        model           = Page
        title           = 'Pages'
    elif is_post:
        model           = Post
        title           = 'Posts'
    elif is_user:
        model           = User
        title           = 'Users'
    elif is_password:
        model           = User
        title           = 'password'

    qs = model.objects.all()
    context={
        'qs'        : qs,
        'page_type'      : title,
        'user_count': User.objects.all().count(),
        'post_count': Post.objects.all().count(),
        'page_count': Page.objects.all().count(),
    }
    context.update(common)
    return render(request, 'accounts/list.html', context)

def edit_content(request, pk):
    #checking weather user is logged in or not
    if not check(request):
        return redirect('login')

    #checking the url
    is_edit_page        = request.path == reverse('edit_page', kwargs={'pk':pk})
    is_edit_post        = request.path == reverse('edit_post', kwargs={'pk':pk})
    is_edit_user        = request.path == reverse('edit_user', kwargs={'pk':pk})
    is_edit_password    = request.path == reverse('edit_password', kwargs={'pk':pk})

    #declaring the model and modelform
    if is_edit_page:
        title           = 'Edit Page'
        model           = Page
        model_form      = PageForm
    elif is_edit_post:
        title           = 'Edit Post'
        model           = Post
        model_form      = PostForm
    elif is_edit_user:
        title           = 'Edit User'
        model           = User
        model_form      = UserUpdateForm
    elif is_edit_password:
        title           = 'Edit Password'
        model           = User
        model_form      = PasswordChangeForm

    #processing the modelform
    model_object        = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        if is_edit_password:
            form            = model_form(data=request.POST, user=model_object)
        else:
            form            = model_form(request.POST, request.FILES or None, instance=model_object)
        
        #Checking the form and saving the object
        if form.is_valid:
            form.save()
            return redirect(request.path)

    if is_edit_password:
        form                = model_form(user=model_object)
    else:
        form                = model_form(instance=model_object)

    context                 = {
        'form'          : form,
        'page_type'     : title,
        'user_count'    : User.objects.all().count(),
        'post_count'    : Post.objects.all().count(),
        'page_count'    : Page.objects.all().count(),
    }
    return render(request, 'accounts/edit.html', context)

@require_POST
def remove_content(request):
    if not check(request):
        return redirect('login')
    page_type = request.POST.get('type')
    if page_type == 'page':
        Page.delete(get_object_or_404(Page, slug=request.POST.get('slug')))
    if page_type == 'post':
        Post.delete(get_object_or_404(Post, slug=request.POST.get('slug')))
    if page_type == 'user':
        User.delete(get_object_or_404(User, pk=request.POST.get('pk')))
    return redirect(request.POST.get('type') + 's')

def add_content(request):
    #checking the url
    is_add_page        = request.path == reverse('add_page')
    is_add_post        = request.path == reverse('add_post')
    is_add_user        = request.path == reverse('add_user')
    is_add_superuser    = request.path == reverse('add_superuser')

    #declaring the model and modelform
    if is_add_page:
        model_form      = PageForm
        title           = 'Add Page' 
    elif is_add_post:
        model_form      = PostForm
        title           = 'Add Post'
    elif is_add_user:
        model_form      = RegisterForm
        title           = 'Add User'
    elif is_add_superuser:
        model_form      = RegisterForm
        title           = 'Add Superuser'

    if request.method == 'POST':
        form            = model_form(request.POST or None, request.FILES or None)
        if form.is_valid():
            if is_add_user or is_add_superuser:
                username = form.cleaned_data["UserName"]
                password = form.cleaned_data["PassWord"]
                firstname = form.cleaned_data["FirstName"]
                lastname = form.cleaned_data["LastName"]
                email = form.cleaned_data["Email"]
                user = User.objects.create_user(username, email, password)
                user.last_name = lastname
                user.first_name = firstname
                if is_add_superuser:
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
            else:
                form.save()
                return redirect(request.path)

    context = {
        'form'          : model_form(),
        'user_count'    : User.objects.all().count(),
        'post_count'    : Post.objects.all().count(),
        'page_count'    : Page.objects.all().count(),
        'page_type'     : title,
    }
    context.update(common)
    return render(request, 'accounts/edit.html', context)

def check(request):
    if request.user.is_superuser:
        return True
    else:
        return False
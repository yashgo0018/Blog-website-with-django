from django.urls import path

from .views import (add_content, dashboard, edit_content, list_content,
                    login_page, logout_page, remove_content)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('posts/', list_content, name='posts'),
    path('pages/', list_content, name='pages'),
    path('users/', list_content, name='users'),
    path('edit_post/<pk>', edit_content, name='edit_post'),
    path('edit_page/<pk>', edit_content, name='edit_page'),
    path('edit_user/<pk>', edit_content, name='edit_user'),
    path('password/', list_content, name='passwords'),
    path('edit_password/<pk>', edit_content, name='edit_password'),
    path('delete_post/', remove_content, name='delete_post'),
    path('delete_page/', remove_content, name='delete_page'),
    path('delete_user/', remove_content, name='delete_user'),
    path('add_user/', add_content, name='add_user'),
    path('add_superuser/', add_content, name='add_superuser'),
    path('add_post/', add_content, name='add_post'),
    path('add_page/', add_content, name='add_page'),
]

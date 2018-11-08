from django.urls import path

from .views import post_detail_view, post_list_view, post_search_handler

urlpatterns = [
    path('', post_list_view, name='list'),
    path('post/<slug>/', post_detail_view, name='post'),
    path('search/', post_search_handler, name='post_search')
]

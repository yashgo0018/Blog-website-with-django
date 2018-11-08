from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from account.views import (subscriber_login_page, subscriber_logout_page,
                           subscriber_register_page)
from pages import views as page_view

urlpatterns = [
    path('admin1/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('blog.urls')),
    path('login/', subscriber_login_page, name="subscriber_login_page"),
    path('register/', subscriber_register_page, name="subscriber_register_page"),
    path('logout/', subscriber_logout_page, name="subscriber_logout_page"),
    path('p/<slug>/', page_view.page_detail_view, name='pages_detail'),
    path('admin/', include('account.urls')),
    path('contact/', page_view.contact_page_view, name="contact_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

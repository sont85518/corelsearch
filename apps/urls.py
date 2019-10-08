from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check$', views.check_iot_status, name='check'),
]
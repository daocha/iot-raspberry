"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse, HttpResponseRedirect

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^device/', lambda x: HttpResponseRedirect('/home/device')),
    url(r'^home/', include('iot_backend.urls')),
    url(r'^', include('iot_backend.urls')),
    #url(r'^$', serve, {'path':'index.html', 'document_root': settings.STATIC_ROOT,}),
]

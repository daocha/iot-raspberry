from django.conf.urls import url
from . import views
from .pages.controlPanel import ControlPanelView
from .pages.home import HomePageView
from .handler.requestHandler import ControlRequest

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    #url(r'^check$', views.check_iot_status, name='check'),
    url(r'^device$', ControlPanelView.as_view(), name='control_panel'),
    url(r'^device/request$', ControlRequest.controlRequest, name='control_request'),
]
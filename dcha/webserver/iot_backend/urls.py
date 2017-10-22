from django.conf.urls import url
from . import views
from .pages.controlPanel import ControlPanelView
from .pages.home import HomePageView
from .handler.requestHandler import ControlRequest

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^check$', views.check_iot_status, name='check'),
    url(r'^control$', ControlPanelView.as_view(), name='control_panel'),
    url(r'^control/request', ControlRequest.controlRequest, name='control_request'),
]
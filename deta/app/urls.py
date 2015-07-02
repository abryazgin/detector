# coding: utf-8

from django.conf.urls import url
from django.contrib.auth import views as authv 
from . import views

urlpatterns = [
    url(r'^login/$', authv.login, {'template_name': 'app/login.html', 'redirect_field_name' : views.UploadView.as_view()}),
    url(r'^logout/$', authv.logout),
    
    url(r'^$', views.UploadView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.ImageView.as_view(), name='image')
]
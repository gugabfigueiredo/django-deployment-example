# -*- coding: utf-8 -*-

from django.conf.urls import url

from fifth_app import views

import os


app_name = os.path.basename(os.path.dirname(__file__))

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^users/', views.users, name='users'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^', views.index, name='index'),
]
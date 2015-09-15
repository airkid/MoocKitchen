"""MoocKitchen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Mooc import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout$', views.logout),
    url(r'^course/([0-9]+)$', views.course_summary),
    url(r'^study_index/([0-9]+)$', views.study_index),
    url(r'^study/$', views.study),
    url(r'^take_course/$', views.take_course),
    url(r'^quiz/([0-9]+)/([0-9]+)/([0-9]+)$', views.take_quiz),
    url(r'^user', views.member),
    url(r'^test/([0-9]+)/([0-9]+)/([0-9]+)$', views.take_test),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^download/', views.get_file),
    url(r'^ttt$', views.ttt),
    url(r'^change_pass$', views.change_pass),
    url(r'^change_info$', views.change_info),
    url(r'^create_message$', views.create_message),
    url(r'^keepnote/$', views.keepnote),
    url(r'^get_messages/$', views.get_messages),
]

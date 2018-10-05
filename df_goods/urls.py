#coding=utf-8
from django.conf.urls import url
from df_goods import views
from django.conf.urls import re_path

urlpatterns=[
    url('index/',views.index),
    url('test/',views.test),
    re_path( '^list-(?P<tid>\d+)',views.list,name="list"),
    re_path( '^detail-(?P<gid>\d+)',views.detail,name="detail")
]
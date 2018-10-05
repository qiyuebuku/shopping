#coding=utf-8
from django.conf.urls import url
from df_user import views
urlpatterns=[
    url('register/',views.register),
    url('login/',views.login),
    url('logout/',views.logout),
    url('addHarvsetAddress/',views.addHarvsetAddress),
    url('user_center_info/',views.user_center_info),
    url('user_center_order/',views.user_center_order),
    url('user_center_site/',views.user_center_site),
]
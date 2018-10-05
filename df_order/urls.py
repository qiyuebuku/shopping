#coding=utf-8
from django.conf.urls import url,re_path
from df_order import views
urlpatterns=[
    url('order/',views.order),
    url('addOrder/',views.addOrder),
    url('payment/',views.payment),
    re_path('^payment-(?P<oid>\d+)',views.payment)
    ]
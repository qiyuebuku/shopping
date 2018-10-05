#coding=utf-8
from django.conf.urls import url
from df_cart import views
from django.conf.urls import re_path

urlpatterns=[
    url('cart/',views.cart),
    url('addCart/',views.addCart),
    url('getCount/',views.getCartCount),
    url('changeAccount/',views.changeAccount),
    url('delCartGoods/',views.delCartGoods),
    url('sumCart/',views.sumCart),
    # re_path( '^list-(?P<tid>\d+)',views.list,name="list"),
]
#coding=utf-8
from django.utils.safestring import mark_safe
from django import template
register=template.Library()
from df_goods import models


@register.simple_tag()
def getNewestFruits(**kwargs):
    """
                <a href="#">鲜芒</a>
                <a href="#">加州提子</a>
                <a href="#">亚马逊牛油果</a>
    :param kwargs:
    :return:
    """
    fruits=models.GoodsTypeInfo.objects.filter(title='水果').first()#获取水果对象
    newestFruits=fruits.goodsinfo_set.order_by('-id')[0:4]
    newestTemp=""
    for i in newestFruits:
        newestTemp='<a href="#">%s</a>'%i.title
    return mark_safe(newestTemp)

# @register.simple_tag()
# def get
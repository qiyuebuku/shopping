#coding=utf-8
from django import template
register=template.Library()

@register.simple_tag
def subtotal(price,count):
    return price*count
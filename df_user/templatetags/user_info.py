#coding=utf-8
from django import template
register=template.Library()

@register.simple_tag
def user_info_list(value):
    if not value:
        return "无"
    else:
        return value

@register.simple_tag
def verifyPay(pay):
    result="已支付" if pay==True else"未支付"
    return result
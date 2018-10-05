#coding=utf-8
from df_order import models as Omodels
from df_user import models as Umodels
from django import forms
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
def getOrderGoodsInfo(request):
    orderAll=Omodels.OrderList.objects.filter(user_id=request.session.get('user_info').get('id')).all()
    OrderDetailList=[]
    for foo in orderAll:
        OrderDetailList.append({'order':foo,'orderDetail':foo.orderdetailinfo_set.all()})
    print( "一共%s张订单"%len(OrderDetailList))
    return OrderDetailList


class addressVerify(forms.ModelForm):
    class Meta:
        model=Umodels.HarvestAddress
        fields="__all__"#显示全部字段
        exclude=["user"]#过滤掉字段
        # 提示信息
        labels={
            'harvestAddress':'收货人地址',
            'harvestName':'收货人姓名',
            'harvestPhone':'收货人电话号码',
        }
        #自定义插件
        widgets={
            'harvestAddress':Fwidgets.Textarea(attrs={'class':'site_area'}),

        }
        #自定义错误信息
        error_messages={
            'harvestPhone':{
                'required':'内容不能为空'
            },
            'harvestName':{
                'required':'内容不能为空'
            },
            'harvestAddress':{
                'required':'内容不能为空'
            },
        }
        #自定义字段类型
        field_classes={
            # 'email':'需要修改成那种类型的字段，注：需要给fields重命名',
        }

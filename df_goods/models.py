from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class GoodsTypeInfo(models.Model):
    title=models.CharField(max_length=32)
    icon=models.ImageField(upload_to="static/goods/GoodTypeInfo/icon",default="static/images/banner02.jpg")
    cover=models.ImageField(upload_to="static/goods/GoodTypeInfo/cover",default="static/images/banner02.jpg")
    isDelete=models.BooleanField(default=False)

class GoodsInfo(models.Model):
    title=models.CharField(max_length=32)#标题
    cover=models.ImageField(upload_to="static/goods/GoodsInfo/cover",default="static/images/banner02.jpg")#封面
    price=models.DecimalField(max_digits=5,decimal_places=2)#价格
    isDelete=models.BooleanField(default=False)#是否删除
    unit=models.CharField(max_length=32)#单位
    click=models.IntegerField()#点击
    synopsis=models.CharField(max_length=220)#介绍
    repertory=models.IntegerField()#库存
    introduce=HTMLField()#内容
    goods_type_info=models.ForeignKey(to="GoodsTypeInfo",to_field="id",on_delete=models.CASCADE)

class RecentGoods(models.Model):
    GoodsInfo=models.ForeignKey(to="GoodsInfo",to_field="id",on_delete=models.CASCADE)
    user=models.ForeignKey(to="df_user.UserInfo",to_field='id',on_delete=models.CASCADE)





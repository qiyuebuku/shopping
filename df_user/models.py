from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username=models.CharField(max_length=32)#用户名
    password=models.CharField(max_length=64)#密码
    email=models.EmailField(max_length=32)#邮箱
    phone=models.CharField(max_length=32,default="")#电话号码

class HarvestAddress(models.Model):
    harvestName = models.CharField(max_length=32, default="")#收货人姓名
    harvestAddress=models.CharField(max_length=255,default="")#收货人地址
    harvestPhone = models.CharField(max_length=32, default="")#收货人号码
    user=models.ForeignKey(to="UserInfo",to_field="id",on_delete=models.CASCADE)







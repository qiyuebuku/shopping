from django.db import models

# Create your models here.


class OrderList(models.Model):
    user=models.ForeignKey(to="df_user.UserInfo",to_field="id",on_delete=models.CASCADE)
    address=models.ForeignKey(to="df_user.HarvestAddress",to_field="id",on_delete=models.CASCADE)
    isPy=models.BooleanField(default=False)
    date=models.DateField(auto_now=True)
    amount=models.IntegerField()
    total=models.DecimalField(max_digits=6,decimal_places=2)

class OrderDetailInfo(models.Model):
    goods=models.ForeignKey(to="df_goods.GoodsInfo",to_field="id",on_delete=models.CASCADE)
    order=models.ForeignKey(to="OrderList",to_field="id",on_delete=models.CASCADE)
    count=models.IntegerField()
    subtotal=models.DecimalField(max_digits=6,decimal_places=2)


from django.db import models

# Create your models here.


class CartInfo(models.Model):
    user=models.ForeignKey(to="df_user.UserInfo",to_field="id",on_delete=models.CASCADE)
    goods=models.ForeignKey(to="df_goods.GoodsInfo",to_field="id",on_delete=models.CASCADE)
    amount=models.IntegerField()

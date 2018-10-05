#coding=utf-8
from df_cart import models as Cmodels
from df_user import models as Umodels
from df_goods import models as Gmodels


#获取购物车的数量
def getShoppingCartCount(user_id):
    userObj=Umodels.UserInfo.objects.filter(id=user_id).first()
    shoppingCartCount=userObj.cartinfo_set.count()
    print('%s的购物车拥有%s件商品'%(userObj.username,shoppingCartCount))
    return shoppingCartCount



#计算购物车总值
def sumAccount(request,list=None):
    uid=request.session.get('user_info').get('id')
    userObj=Umodels.UserInfo.objects.filter(id=uid).first()
    shoppingCartCount = userObj.cartinfo_set.values().all()
    sum=0
    if not list:list=[]
    for foo in shoppingCartCount:
        if not str(foo["id"]) in list:
            goods=Gmodels.GoodsInfo.objects.filter(id=foo["goods_id"]).first()
            sum+=goods.price*foo["amount"]
    return(sum)

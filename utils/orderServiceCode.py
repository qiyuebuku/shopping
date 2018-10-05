#coding=utf-8
from df_order import models as Omodels
from df_user import models as Umodels
from df_goods import models as Gmodels
from df_cart import models as Cmodels
def createOrder(request,list):
    user=Umodels.UserInfo.objects.filter(id=request.session.get('user_info').get('id')).first()
    Omodels.OrderList.objects.create(user_id=request.session.get('user_info').get('id'),
                                     )

def getGoodsInfo(request,list):
    goodsListInfo = []
    for i in list:
        cart=Cmodels.CartInfo.objects.filter(id=i).first()
        try:
            goods=cart.goods
        except AttributeError as e:
            print('购物车里面没有物品')
        goodsListInfo.append({'goods':goods,'id':cart.id,'amount':cart.amount,'account':goods.price*cart.amount})
    return goodsListInfo
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from df_cart import models
from df_user import models as Umodels
from df_goods import models as Gmodel
import json
from utils import cartServiceCode
from utils import verifycation
# Create your views here.
@verifycation.auth
def cart(request):
    if request.method=="GET":
        user=Umodels.UserInfo.objects.filter(id=request.session.get('user_info').get('id')).first()
        cart=user.cartinfo_set.values().all()
        goodsInfoList=[]
        shoppingCartCount=cartServiceCode.getShoppingCartCount(request.session.get('user_info').get('id'))
        Account = cartServiceCode.sumAccount(request)
        for i in cart:
            goodsInfoList.append({'goods':Gmodel.GoodsInfo.objects.filter(id=i["goods_id"]).first(),
                                  'amount':i.get('amount'),
                                  'id':i.get('id'),
                                  })
        return render(request,"df_cart/cart.html",{'title':"天天生鲜-购物车",'goodsList':goodsInfoList,'cartCount':shoppingCartCount,'account':Account,})
@verifycation.auth
def addCart(request):
    if request.method=="GET":
        pass
    elif request.method=="POST":
        ret={'state':True,'error':None,'data':None}
        try:
            goodsCount = request.POST.get('count')
            goods_id = request.POST.get('id')
            user_id = request.session.get('user_info').get('id')
            if models.CartInfo.objects.filter(goods_id=goods_id).count()==0:

                models.CartInfo.objects.create(user_id=user_id, goods_id=goods_id, amount=goodsCount)
            else:
                amount=models.CartInfo.objects.filter(goods_id=goods_id).first().amount
                models.CartInfo.objects.filter(goods_id=goods_id).update(amount=amount+int(goodsCount))
            user_CartCount = Umodels.UserInfo.objects.filter(id=user_id).first().cartinfo_set.count()
            ret["data"] = {'count': user_CartCount}
            print(
                '用户Id：%s，将物品Id：%s，加入到了他的购物车，加入物品数量：%s，购物车物品数量：%s' % (user_id, goods_id, goodsCount, user_CartCount))

        except Exception as e:
            ret["state"]=False
            ret["error"]=e
            print("添加购物车错误：",ret)
        return HttpResponse(json.dumps(ret))

def getCartCount(request):
    if request.session.get('status')==True:
        cartCount = cartServiceCode.getShoppingCartCount(request.session.get('user_info').get('id'))
    else:
        cartCount=0
    return HttpResponse(cartCount)
@verifycation.auth
def changeAccount(request):
    cid=request.GET.get('id')
    amount=request.GET.get('count')
    models.CartInfo.objects.filter(id=cid).update(amount=amount)
    Account=cartServiceCode.sumAccount(request)
    return HttpResponse(Account)
@verifycation.auth
def delCartGoods(request):
    gid=request.POST.get('gid')
    ret={'status':True,'error':None,'data':None}
    try:
        result=models.CartInfo.objects.filter(id=gid).delete()
        shoppingCartCount=cartServiceCode.getShoppingCartCount(request.session.get('user_info').get('id'))
        ret["data"]=shoppingCartCount
    except Exception as e:
        ret["status"]=False
        ret["error"]=e
    return HttpResponse(json.dumps(ret))

def sumCart(request):
    cartIdList=request.GET.getlist('list[]')
    sum=cartServiceCode.sumAccount(request,cartIdList)
    return HttpResponse(sum)

from django.shortcuts import render,HttpResponse,redirect
from df_user import models as Umodels
from df_order import models as Omodels
from df_cart import models as Cmodels
from df_goods import models as Gmodels
from utils import orderServiceCode
import json
# Create your views here.

def order(request):
    if request.method == "GET":
        goodsListInfo=[]
        amount=0
        account=0
        user_info = request.session.get('user_info')  # 获取用户信息
        addressList = Umodels.UserInfo.objects.filter(
            id=user_info.get('id')).first().harvestaddress_set.values().all()  # 当前用户的所有收获地址
        gid=request.session.get('gid')
        if not gid:
            list=request.session.get('list')
            goodsListInfo = orderServiceCode.getGoodsInfo(request, list)  # 获取所有被选中的物品信息
            amount=request.session["amount"]
            account=request.session["account"]
        else:
            count=request.session.get('count')
            goods=Gmodels.GoodsInfo.objects.filter(id=gid).first()
            xiaoji=("%.2f"%round(float(count)*float(goods.price)))
            goodsListInfo.append({'goods':goods , 'id': 1, 'amount': count, 'account': xiaoji })
            account=1
            amount=xiaoji
        return render(request, "df_order/place_order.html", {'title': "天天生鲜-提交订单",
                                                             "goodsListInfo": goodsListInfo,
                                                             "amount": amount,
                                                             "account": account,
                                                             "addressList": addressList,
                                                             })
    elif request.method=="POST":
        ret={"status":True,"error":None,"data":None}
        try:
            gid=request.POST.get('gid')
            if not gid:
                print('购物车订单')
                list=request.POST.getlist('list[]')#所右被选中的购物车ID
                amount=request.POST.get('amount')#共计费用
                account=request.POST.get('account')#共计数量
                #将从前端获取到的内容写入到Session中，以便显示时使用
                request.session['list']=list
                request.session["amount"]=amount
                request.session["account"]=account
            else:
                print('单个订单')
                request.session["count"]=request.POST.get('count')
                request.session["gid"]=gid
        except Exception as e:
            ret["status"]=False
            ret["error"]=e
        return HttpResponse(json.dumps(ret))

def addOrder(request):
    if request.method=="GET":
        pass
    elif request.method=="POST":
        ret={'status':True,'error':None,'data':None}
        list=request.session.get('list')
        gid=request.session.get('gid')
        try:
            goodsListInfo=[]
            account=0
            amount=0
            if not gid:
                goodsListInfo = orderServiceCode.getGoodsInfo(request,list)  # 获取所有被选中的物品信息
                amount=request.session.get("account")#合计数量
                print('gid')
                account= request.session.get("amount")  # 合计价格
                gid=request.session.get('gid')
            elif gid:
                print('else')
                count = request.session.get('count')
                goods = Gmodels.GoodsInfo.objects.filter(id=gid).first()
                xiaoji = ("%.2f" % round(float(count) * float(goods.price)))
                goodsListInfo.append({'goods': goods, 'id': 1, 'amount': count, 'account': xiaoji})
                account = xiaoji
                amount = 1
                print(amount,account)
                request.session["gid"] = None
            #创建订单信息
            order_list=Omodels.OrderList(
                 user_id=request.session.get('user_info').get('id'),#用户id
                 address_id=request.POST.get('pid'),#地址id
                 isPy=False,#是否支付
                 amount=amount,
                 total=account)#总计钱
            order_list.save()
            for g in goodsListInfo:
                Omodels.OrderDetailInfo.objects.create(
                     goods_id=g.get('goods').id,
                     order_id=order_list.id,
                     count=g.get('amount'),
                     subtotal=g.get('account'),
                )
        except Exception as e:
            ret["status"]=False
            ret["error"]=e
        #如果添加订单没有问题，那么就删除购物车的内容
        shoppingCartAll=Cmodels.CartInfo.objects.all()
        if list:
            for cart in shoppingCartAll:
                if str(cart.id) in list:
                    Cmodels.CartInfo.objects.filter(id=cart.id).delete()
            request.session["list"]=None
        return HttpResponse(json.dumps(ret))

def payment(request,oid):
    Omodels.OrderList.objects.filter(id=oid).first().delete()
    return redirect('/user/user_center_order/')






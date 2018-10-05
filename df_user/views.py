from django.shortcuts import render,redirect,HttpResponse
from utils import verifycation
from df_user import models
from django.utils.safestring import mark_safe
from utils import userServiceCode
# Create your views here.

# 注册
def register(request):
    verify=verifycation.registerVerify
    if request.method=="GET":
        verify = verify()
        return render(request,"df_user/register.html",{'title':"天天生鲜",'verify':verify})
    elif request.method=="POST":
        verify=verify(request.POST)
        if verify.is_valid():
            models.UserInfo.objects.create(username=verify.cleaned_data['username'],
                                           password=verify.cleaned_data["password"],
                                           email=verify.cleaned_data["email"])
            return redirect('/user/login/')
        else:
            print(verify.errors)
            return render(request, "df_user/register.html", {'title': "天天生鲜", 'verify': verify})
# 登陆
def login(request):
    if request.method=="GET":
        verify=verifycation.loginVerigy()
        return render(request,"df_user/login.html",{'title':"天天生鲜",'verify':verify})
    elif request.method=="POST":
        verify = verifycation.loginVerigy(request.POST)
        if verify.is_valid():
            count=models.UserInfo.objects.filter(username=verify.cleaned_data["username"],
                                                 password=verify.cleaned_data["password"]).count()
            if count==0:
                verify.errors["password"]="用户名或者密码错误"
                print(verify.errors)
                return render(request, "df_user/login.html", {'title': "天天生鲜", 'verify': verify})
            # 获取用户详细信息
            user_info = models.UserInfo.objects.values().filter(username=verify.cleaned_data["username"],
                                                                password=verify.cleaned_data["password"]).first()
            request.session["status"]=True
            request.session["user_info"]=user_info
            request.session.set_expiry(0)
            print(request.session["user_info"]["username"],':登陆成功')
            return redirect("/user/user_center_info/")
        else:
            print(verify.errors)
            return render(request, "df_user/login.html", {'title': "天天生鲜", 'verify': verify})
@verifycation.auth#用于验证session是否激活
# 个人信息
def user_center_info(request):
    if request.method=="GET":
        jump=mark_safe("""
        <li><a href="/user/user_center_info/" class="active">· 个人信息</a></li>
                    <li><a href="/user/user_center_order/">· 全部订单</a></li>
                    <li><a href="/user/user_center_site/">· 收货地址</a></li>
        """)
        user=models.UserInfo.objects.filter(id=request.session.get('user_info')["id"]).first()
        ObjRecents=user.recentgoods_set.order_by('-id')[0:5]
        RecentsGoods=[]
        for recent in ObjRecents:
            RecentsGoods.append(recent.GoodsInfo)
        return render(request,"df_user/user_center_info.html",{
            'title':"用户中心-个人信息",
            "left_menu_con":jump,
            'RecentsGoods':RecentsGoods
        })
@verifycation.auth#用于验证session是否激活
# 全部订单
def user_center_order(request):
    if request.method=="GET":
        jump = mark_safe("""
                <li><a href="/user/user_center_info/" >· 个人信息</a></li>
                            <li><a href="/user/user_center_order/" class="active">· 全部订单</a></li>
                            <li><a href="/user/user_center_site/">· 收货地址</a></li>
                """)
        OrderDetailList=userServiceCode.getOrderGoodsInfo(request)
        return render(request,"df_user/user_center_order.html",{
            'title':"用户中心-全部订单","left_menu_con":jump,
            'OrderDetailList':OrderDetailList
        })
@verifycation.auth#用于验证session是否激活
# 收货地址
def user_center_site(request):
    if request.method=="GET":
        jump = mark_safe("""
                <li><a href="/user/user_center_info/" >· 个人信息</a></li>
                            <li><a href="/user/user_center_order/">· 全部订单</a></li>
                            <li><a href="/user/user_center_site/" class="active">· 收货地址</a></li>
                """)
        obj=userServiceCode.addressVerify()
        user=models.UserInfo.objects.filter(id=request.session.get('user_info').get('id')).first()
        addressList =user.harvestaddress_set.values().all() # 当前用户的所有收货地址
        return render(request,"df_user/user_center_site.html",{'title':"用户中心-收获地址",
                                                               "left_menu_con":jump,
                                                               'obj':obj,
                                                               'addressList':addressList
                     })

def logout(request):
    request.session.clear()
    return redirect('/user/login/')


def addHarvsetAddress(request):
    obj=userServiceCode.addressVerify(request.POST)
    if obj.is_valid():
        models.HarvestAddress.objects.create(harvestName=obj.cleaned_data["harvestName"],
                                             harvestAddress=obj.cleaned_data["harvestAddress"],
                                             harvestPhone=obj.cleaned_data["harvestPhone"],
                                             user_id=request.session.get('user_info').get('id'))
    else:
        print("添加地址失败",obj.errors)
    return redirect('/user/user_center_site/')
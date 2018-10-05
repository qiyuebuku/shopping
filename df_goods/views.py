from django.shortcuts import render
from utils import generate
from django.utils.safestring import mark_safe
from df_goods import models

# Create your views here.

def test(request):
    return render(request,"test.html")
def index(request):
    if request.method=="GET":
        GoodsInfo=generate.GenerateIndex()
        body=GoodsInfo.getBody()

        return render(request,
                      "df_goods/index.html",{
                      'title':"给我家秀宝宝看的-首页",
                       'body':body,
                      }
        )
    elif request.method=="POST":
        pass

def list(request,tid):
    if request.method=="GET":
        s=request.GET.get('s','1')
        ListInfo=generate.GenerateList(request,tid,s)
        body=ListInfo.getBody()
        return render(request,"df_goods/list.html",{'title':"天天生鲜-商品列表",'body':body})

def detail(request,gid):
    if request.method=="GET":
        DetailInfo = generate.GenerateDetail(gid)
        if request.session.get('status'):
            user_id=request.session.get('user_info',None).get('id')
            models.RecentGoods.objects.create(GoodsInfo_id=gid,user_id=user_id)
            DetailInfo.createClick(gid)
        body=DetailInfo.getBody()
        return render(request,"df_goods/detail.html",{'body':body})


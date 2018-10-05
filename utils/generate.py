# coding=utf-8
from df_goods import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from utils import pagination


class GenerateIndex(object):
    def __init__(self):
        # 获得所有商品种类
        Type = models.GoodsTypeInfo.objects.all()
        self.goodsType = Type

    # 创建主页各分类标题
    def createTitle(self):
        titleObj = self.obj  # 获取当前类型的对象
        title = titleObj.title  # 标题
        newestFruits = titleObj.goodsinfo_set.order_by('-id')[0:4]  # 反查出这个类型，最新的四款商品
        newestGoods = ""  # 用于拼接最新四款产品的HTML
        for i in newestFruits:
            url2 = reverse('detail', kwargs={'gid': i.id})  # 反向获取URLS的地址
            newestGoods += '<a href="%s">%s</a>' % (url2,i.title)
        url2 = reverse('list', kwargs={'tid': titleObj.id})  # 反向获取URLS的地址
        titeId = str(titleObj.id)
        # 最终返回这个
        typeTitle = '''
        <div class="list_title clearfix">
            <h3 class="fl" id="model0''' + titeId + '''">''' + title + '''</h3>
            <div class="subtitle fl">
                <span>|</span>
                ''' + newestGoods + '''
            </div>
            <a href="''' + url2 + '''" class="goods_more fr" id="fruit_more">查看更多 ></a>
        </div>
        '''
        return typeTitle

    def createCover(self):
        # print("121",type(self.obj.cover.__str__()))
        temp = '<div class="goods_banner fl"><img src="/' + self.obj.cover.__str__() + '"></div>'
        return temp

    def createGoods(self):
        obj = self.obj
        newestFruits = obj.goodsinfo_set.order_by('-id')[0:4]  # 反查出这个类型，最新的四款商品
        goodInfo = '<ul class="goods_list fl">'
        for goods in newestFruits:
            url2 = reverse('detail', kwargs={'gid': goods.id})  # 反向获取URLS的地址
            temp = """
                <li>
                    <h4><a href="%s">%s</a></h4>
                    <a href="%s"><img src="/%s"></a>
                    <div class="prize">¥ %s</div>
                </li>
            """ % (url2,#跳转地址
                   goods.title,#标题
                   url2,#跳转地址
                   goods.cover,#封面图片
                   goods.price#价格
                   )
            goodInfo += temp
        goodInfo += '</ul>'
        return goodInfo

    def getBody(self):
        body = ""
        for goodsType in self.goodsType:
            self.obj = goodsType
            title = self.createTitle()  # 创建Title
            cover = self.createCover()  # 创建
            goods = self.createGoods()  # 创建商品信息
            body += """
            <div class="list_model">
               %s
               <div class="goods_con clearfix">
                 %s
                 %s
               </div>
            </div>
            """ % (title, cover, goods,)
        return mark_safe(body)


class GenerateList(object):
    def __init__(self, request, tid,s):
        self.tid = tid
        self.s=s
        self.request = request
        self.typeObj = models.GoodsTypeInfo.objects.filter(id=tid).first()
        print()

    def createPathNavigation(self):
        pathNavigation = """
        <div class="breadcrumb">
            <a href="/goods/index">全部分类</a>
            <span>></span>
            <a href="#">%s</a>
	    </div>
        """ % (self.typeObj.title)
        return pathNavigation

    def createNewProductsGoods(self):
        newestGoodsObj = self.typeObj.goodsinfo_set.order_by('-id')[0:2]
        newProducts = ""
        for goods in newestGoodsObj:
            url2 = reverse('detail', kwargs={'gid': goods.id})  # 反向获取URLS的地址
            cover = goods.cover
            title = goods.title
            price = goods.price
            newProducts += '''
            <li>
                <a href="%s"><img src="/%s"></a>
                <h4><a href="%s">%s</a></h4>
                <div class="prize">￥%s</div>
            </li>
            ''' % (url2,cover,url2, title, price)
        return newProducts

    def createGoods(self, **kwargs):
        print('list显示数据',kwargs['start'],"-",kwargs["end"])
        goodsAllObj=""
        if self.s=='1':
            goodsAllObj = self.typeObj.goodsinfo_set.order_by('-id')[kwargs['start']:kwargs['end']]
        elif self.s=='2':
            goodsAllObj = self.typeObj.goodsinfo_set.order_by('-price')[kwargs['start']:kwargs['end']]
        elif self.s=='3':
            goodsAllObj = self.typeObj.goodsinfo_set.order_by('-click')[kwargs['start']:kwargs['end']]
        goodsAll = ""
        for goods in goodsAllObj:
            url2 = reverse('detail', kwargs={'gid': goods.id})  # 反向获取URLS的地址
            cover = goods.cover
            title = goods.title
            price = goods.price
            unit = goods.unit
            goodsAll += """
             <li>
                <a href="%s"><img src="/%s"></a>
                <h4><a href="%s">%s</a></h4>
                <div class="operate">
                    <span class="prize">￥%s</span>
                    <span class="unit">%s</span>
                    <a href="" i='%s' class="add_goods" title="加入购物车"></a>
                </div>
            </li>
            """ % (url2,cover,url2, title, price,unit,goods.id)
        return goodsAll
    def createSort(self):
        list=['','<a href="%s" class="">默认</a>','<a href="%s" class="">价格</a>','<a href="%s" class="">人气</a>']
        list[int(self.s)]=list[int(self.s)].replace('class=""','class="active"')
        list="".join(list)%(
            "/goods/list-" + str(self.typeObj.id) + "?s=1",
            "/goods/list-" + str(self.typeObj.id) + "?s=2",
            "/goods/list-" + str(self.typeObj.id) + "?s=3",
        )
        sort="""
        <div class="sort_bar">"""+list+""""
        </div>
        """
        return sort
    def getBody(self):
        current_page = int(self.request.GET.get('p', 1))
        count = self.typeObj.goodsinfo_set.all().count()
        page_obj = pagination.Page(current_page, count, 5, 10)

        pathNaviGation = self.createPathNavigation()  # 导航路径
        newProducts = self.createNewProductsGoods()  # 新品推荐
        goodsAll = self.createGoods(start=page_obj.start, end=page_obj.end)  # 所有商品
        sort=self.createSort()#物品显示方式
        url=reverse('list',kwargs={'tid':self.typeObj.id})
        souce='/goods/list-%s?s=%s&&'%(self.tid,self.s)
        body = """
            %s
            <div class="main_wrap clearfix">
                <div class="l_wrap fl clearfix">
                    <div class="new_goods">
                        <h3>新品推荐</h3>
                        <ul>
                        %s
                        </ul>
                    </div>
                </div>
        
                <div class="r_wrap fr clearfix">
                    %s
                    <ul class="goods_type_list clearfix">
                        %s
                    </ul>
                    <div class="pagenation">
                        %s
                    </div>
                </div>
            </div>
            """ % (pathNaviGation,
                   newProducts,
                   sort,
                   goodsAll,
                   page_obj.page_str(souce,"p"))
        return mark_safe(body)


class GenerateDetail(object):

    def __init__(self, gid):
        self.gid = gid
        self.goods = models.GoodsInfo.objects.filter(id=gid).first()

    def createPathNavigation(self):
        goodsType = self.goods.goods_type_info
        url2 = reverse('list', kwargs={'tid': goodsType.id})  # 反向获取URLS的地址
        pathNavigation = """
        <div class="breadcrumb">
            <a href="/goods/index">全部分类</a>
            <span>></span>
            <a href="%s">%s</a>
            <span>></span>
            <a href="#">商品详细</a>
        </div>
        """ % (url2, goodsType.title)
        return pathNavigation

    def createCover(self):
        cover = '<div class="goods_detail_pic fl" ><img style="width:300px;height:300px;" src="/%s"></div>' % self.goods.cover
        return cover

    def createGoodsInfo(self):
        goods = self.goods
        title = goods.title
        synopsis = goods.synopsis
        price = goods.price
        unit = goods.unit
        goodsInfo = '''
            <h3>''' + title + '''</h3>
            <p>''' + synopsis + '''</p>
            <div class="prize_bar">
                <span class="show_pirze" >¥<em id="price">''' + str(price) + '''</em></span>
                <span class="show_unit">单  位：''' + unit + '''</span>
            </div>
        '''
        return goodsInfo
    def createIntroduce(self):
        introduce="""
        <dl>
            <dt>商品详情：</dt>
            <dd>%s</dd>
        </dl>
        """%self.goods.introduce
        return introduce
    def createNewProductsGoods(self):
        newestGoodsObj = self.goods.goods_type_info.goodsinfo_set.order_by('-id')[0:2]
        newProducts = ""
        for goods in newestGoodsObj:
            url2 = reverse('detail', kwargs={'gid': goods.id})  # 反向获取URLS的地址
            cover = goods.cover
            title = goods.title
            price = goods.price
            newProducts += '''
            <li>
                <a href="%s"><img src="/%s"></a>
                <h4><a href="%s">%s</a></h4>
                <div class="prize">￥%s</div>
            </li>
            ''' % (url2,cover, url2,title, price)
        return newProducts
    def createClick(self,gid):
        click=models.GoodsInfo.objects.filter(id=gid).first().click
        models.GoodsInfo.objects.filter(id=gid).update(click=click+1)
    def getBody(self):
        pathNavigation = self.createPathNavigation()
        cover = self.createCover()
        goodsInfo = self.createGoodsInfo()
        introduce=self.createIntroduce()
        newProducts=self.createNewProductsGoods()
        body = """
            <div class="goods_detail_con clearfix">
		        """+pathNavigation+cover+"""
               	<div class="goods_detail_list fr">"""+goodsInfo+"""
                    <div class="goods_num clearfix">
                        <div class="num_name fl">数 量：</div>
                        <div class="num_add fl" >
                            <input type="text" id="count" class="num_show fl" value="1">
                            <a  id="insert" style="cursor:pointer;" class="add fr">+</a>
                            <a  id="reduce" style="cursor:pointer;" class="minus fr">-</a>
                        </div>
                        </span>
                    </div>
                    <div class="total" >总价：<em id="totalPrice">16.80元</em></div>
                    <div class="operate_btn">
                        <a href="javascript:;" class="buy_btn">立即购买</a>
                        <a href="#" class="add_cart"i='"""+self.gid+"""' id="add_cart">加入购物车</a>
                    </div>
                </div>
            </div>
	<div class="main_wrap clearfix">
		<div class="l_wrap fl clearfix">
			<div class="new_goods">
				<h3>新品推荐</h3>
				<ul>
					"""+newProducts+"""
				</ul>
			</div>
		</div>

		<div class="r_wrap fr clearfix">
			<ul class="detail_tab clearfix">
				<li class="active">商品介绍</li>
				<li>评论</li>
			</ul>

			<div class="tab_content">"""+introduce+"""

			</div>

		</div>
	</div>
	
    """
        return mark_safe(body)

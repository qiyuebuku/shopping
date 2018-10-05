#coding=utf-8
from django.utils.safestring import mark_safe
# 自定义分页，具体推到过程看当前项目下的“推到分页.txt”
class Page(object):
    # 功能：自动分页
    # current_pate:当前页数
    # data_count:一共有多少条数据
    # pager_nu:每次显示多少页
    # per_page_count:每页能显示多少条数据
    def __init__(self,current_page,data_count,pager_num=11,per_page_count=10):
        self.current_page=current_page
        self.data_count=data_count
        self.pager_num=pager_num
        self.per_page_count=per_page_count

    @property
    def count(self):
        count, remainder = divmod(self.data_count, self.per_page_count)
        if remainder:
            count += 1
        return count
    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count
    @property
    def end(self):
        return self.current_page*self.per_page_count
    def page_str(self,base,str="?p"):
        """
        base:是你的页面地址，如：/goods/list-1
        str:是你想要以那种样式，给你的页面地址加参数，如：她默认是?p
        :param base:
        :param str:
        :return:
        """
        page_list = []
        if self.count < self.pager_num:
            start_index = 1
            end_index = self.count + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.count:
                    end_index = self.count + 1
                    start_index = self.count - self.pager_num + 1

        start_index = int(start_index)
        end_index = int(end_index)
        if self.current_page > 1:
            prev = "<a class='page' href='%s%s=%s'>上一页</a>" % (base,str,self.current_page - 1)
        else:
            prev = "<a class='page' href='javascript:void(0);'>上一页</a>"
        page_list.append(prev)
        for i in range(start_index, end_index):
            if self.current_page == i:
                temp = ("<a class='page active' href='%s%s=%s'>%s</a>" % (base,str,i, i))
            else:
                temp = ("<a class='page' href='%s%s=%s'>%s</a>" % (base,str,i, i))
            page_list.append(temp)
        if self.current_page < self.count:
            nex = "<a class='page' href='%s%s=%s'>下一页</a>" % (base,str,self.current_page + 1)
        else:
            nex = "<a class='page' href='javascript:void(0);'>上一页</a>"
        page_list.append(nex)

        jump = """
            <input id="input" type='text'/>
            <input type="button" onclick='jumpTo("%s%s=");' value="GO"/>
            <script>
                function jumpTo(s){
                    var val=document.getElementById('input').value;
                    location.href=s+val;
                }
            </script>
        """%(base,str)

        page_list.append(jump)
        page_list = mark_safe("".join(page_list))
        return page_list
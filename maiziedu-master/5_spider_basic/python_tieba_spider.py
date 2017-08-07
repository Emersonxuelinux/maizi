# -*- coding:utf-8 -*-
'''
爬取python贴吧里面用户名及头像图片信息.爬取网页链接:http://tieba.baidu.com/f?kw=python&fr=ala0&tpl=5，只需要爬取该贴吧链接里面的头像即可,用户名作为头像图片的名称。
'''


'''
要获取的html标签范围：
<div class="threadlist_lz clearfix"> # 这是第一个定位标签
    <div class="threadlist_title pull_left j_th_tit ">
        <a href="/p/4612057728" title="【腾讯课堂免费Python直播课程】秒杀一切Python视频资料" target="_blank" class="j_th_tit ">【腾讯课堂免费Python直播课程】秒杀一切Python视频资料</a>
    </div>
    <div class="threadlist_author pull_right">


    # 这是第二个定位标签，其中title是作者


    <span class="tb_icon_author " title="主题作者: openlabczx" data-field="{&quot;user_id&quot;:1087985062}">
        <i class="icon_author"></i>


        # 这是最后一个定位标签，其中href就是用户首页，可以获取头像，注意要拼接一下


        <a data-field="{&quot;un&quot;:&quot;openlabczx&quot;}" class="frs-author-name j_user_card " href="/home/main/?un=openlabczx&amp;ie=utf-8&amp;fr=frs" target="_blank">openlabczx</a>
        <span class="icon_wrap  icon_wrap_theme1 frs_bright_icons "></span>    
    </span>
    <span class="pull-right is_show_create_time" title="创建时间">6-15</span>
</div>
            </div>
'''

import requests
import re
from HTMLParser import HTMLParser
import pdb
import chardet

class UserParser(HTMLParser):
    def __init__(self): # 一次请求只初始化一次
        HTMLParser.__init__(self)
        self.in_div = False
        self.in_span = False
        self.uniq = []  # 用来避免重复抓取用户名
        self.uniq_flag = False
        self.user_list =[]
        self.current_user = {}
         
    def handle_starttag(self,tag,attrs):

        # 定义一个内部函数用来解析属性
        def _attr(attrlist, attrname):  # 传入属性列表和要获取属性值的属性名
            for attr in attrlist:  # 取出的attr是元组，0下标指属性名，1下标指向属性值
                if attr[0] == attrname:
                    return attr[1]
            return None
            
        # 确认用户名所在的div标签
        if tag == 'div' and _attr(attrs, 'class') == 'threadlist_lz clearfix':
            # pdb.set_trace()
            # print tag+':' + _attr(attrs, 'class')
            self.in_div = True

        # 轮到其中的span标签;只要title存在且包含“主题作者”四个字，肯定是目标span
        if self.in_div and tag == 'span' and _attr(attrs, 'title')!=None and u'\u4e3b\u9898\u4f5c\u8005' in _attr(attrs, 'title'): 
            # 和之前一样，提取用户名
            name = re.split(': ', # 把属性值分段
                    _attr(attrs, 'title')
                    .encode("utf-8"))[1].decode("utf-8")
            # 用户名不重复时才抓取
            if name not in self.uniq:
                self.uniq.append(name)
                self.current_user['name'] = name
                self.uniq_flag = True
            self.in_span = True


        # 获取用户主页链接，在目标span中获取class存在且包含'frs-author-name'的a标签即可
        if self.in_span and tag == 'a' and _attr(attrs, 'class')!=None and 'frs-author-name' in _attr(attrs, 'class'):
            # 拼接后获取用户信息
            user_link = 'http://tieba.baidu.com' + _attr(attrs, 'href')
            # print user_link
            # 用户名不重复时才放入链接
            if self.uniq_flag:
                self.current_user['user_link'] = user_link
                self.user_list.append(self.current_user)
                self.uniq_flag = False
            self.current_user = {}
            self.in_div = False
            self.in_span = False

# 用户头像解析类
class UserInfoParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)  #此处你忘记初始化，所以造成rawdata的错误
        self.in_a = False

    # 定义一个内部函数用来解析属性
    def _attr(self,attrlist, attrname):  # 传入属性列表和要获取属性值的属性名
        for attr in attrlist:  # 取出的attr是元组，0下标指属性名，1下标指向属性值
            if attr[0] == attrname:
                return attr[1]
        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and self._attr(attrs, 'class') == 'userinfo_head':
            self.in_a = True

    def handle_startendtag(self, tag, attrs):
        if tag == 'img' and self.in_a:
            self.img_url = self._attr(attrs, 'src') #之前这里写成了两个等号，提示


# 提示：写程序的时候最好把功能分开（注意解耦）
# 1，先获取用户页面链接
# 2，再根据用户链接获取用户头像的img_url


def retrieve_users():
    url = 'http://tieba.baidu.com/f?kw=python&fr=ala0&tpl=5'
    r = requests.get(url)
    parser = UserParser()
    # print chardet.detect(r.content)
    parser.feed(r.content.decode('utf-8'))
    userinfoparser = UserInfoParser()
    for user in parser.user_list:
        # print "User: ",user
        response = requests.get(user['user_link'])
        userinfoparser.feed(response.content.decode('GB18030'))
        user['user_link'] = userinfoparser.img_url
        # 初始化实例
        userinfoparser.reset()
        
    return parser.user_list

if __name__ == '__main__':
    l = retrieve_users()
    for key in l:
        print key['name']," -- ",key['user_link']

# -*- coding: utf-8 -*-
import requests
from HTMLParser import HTMLParser


class DoubanClient(object):
    def __init__(self):
        object.__init__(self)
        # 第一次设置头信息，为了获取服务器返回的登陆界面信息，后面还会再加入伪装信息
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
                   'origin': 'http://www.douban.com'}
        
        # create requests session
        self.session = requests.session()
        self.session.headers.update(headers)


    def login(self, username, password,
              source='index_nav',
              redir='http://www.douban.com/',
              login='登录'):

        url = 'https://www.douban.com/accounts/login'
        # 使用session来发送请求，第一次是get方式，用于获取服务器返回的登陆界面
        r = self.session.get(url)

        # 又见元组解包写法，用元组一次给两个变量赋值
        (captcha_id, captcha_url) = _get_captcha(r.content)
        
        # 如果发送请求获得了验证码，就要求输入人眼识别后的验证码内容
        if captcha_id:
            captcha_solution = raw_input('please input solution for captcha [%s]:' % captcha_url)
        

        # post login request
        data = {'form_email': username,
                'form_password': password,
                'source': source,
                'redir': redir,
                'login': login}

        # 如果有验证码信息，就把验证码信息加入到要post的数据中
        if captcha_id:
            data['captcha-id'] = captcha_id
            data['captcha-solution'] = captcha_solution
        
        # 第二次设置头信息，这次是设置更加完整，准备post登陆信息给服务验证
        headers = {'referer': 'http://www.douban.com/accounts/login?source=main',
                   'host': 'accounts.douban.com'}
        

        
        
        # 第二次发送请求，把验证码信息，用户名，密码等信息都用post方式发给服务器
        self.session.post(url, data=data, headers=headers)
        print(self.session.cookies.items())

    def edit_signature(self, username, signature):
        url = 'https://www.douban.com/people/%s/' % username
        # 第一次访问用户主页，用get获取信息，这个不涉及安全，不需要post
        r = self.session.get(url)
        # 根据我们分析的url流程，从页面中获取ck的value值，并放入要post的数据中
        data = {'ck': _get_ck(r.content), 'signature': signature}
        url = 'https://www.douban.com/j/people/%s/edit_signature' % username
        headers = {'referer': url,
                   'host': 'www.douban.com',
                   'x-requested-with': 'XMLHttpRequest'}
        r = self.session.post(url, data=data, headers=headers)
        print(r.content)


def _attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None


def _get_captcha(content):

    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_id = None  # 默认情况下验证码信息为空
            self.captcha_url = None


        # 重写htmlparser这个方法来解析出验证码信息
        def handle_starttag(self, tag, attrs):
            if tag == 'img' and _attr(attrs, 'id') == 'captcha_image' and _attr(attrs, 'class') == 'captcha_image':
                self.captcha_url = _attr(attrs, 'src')

            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'captcha-id':
                self.captcha_id = _attr(attrs, 'value')

    p = CaptchaParser()
    p.feed(content)
    return p.captcha_id, p.captcha_url


def _get_ck(content):
    # 构造一个解析器专门用于解析Ck值
    class CKParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck = None

        def handle_starttag(self, tag, attrs):
            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'ck':
                self.ck = _attr(attrs, 'value')

    p = CKParser()
    p.feed(content)
    return p.ck


if __name__ == '__main__':
    c = DoubanClient()
    c.login('hughohoho@gmail.com', 'n,f4f6DRzroUZ(bLrWzG')
    # 一定要先登录再修改
    c.edit_signature('113667643', 'python 爬虫基础')

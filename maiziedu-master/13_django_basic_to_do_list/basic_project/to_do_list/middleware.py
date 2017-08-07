import re
from django.shortcuts import redirect

class CheckBrowser(object):
    # Request预处理函数,调用时机在 Django 接收到 request
    # 之后，但仍未解析URL以确定应当运行的 view 之前。Django 向它传入相应的
    # HttpRequest 对象，以便在方法中修改。
	def process_request(self,request):
		# 获取浏览器信息
		agent = (request.META['HTTP_USER_AGENT'])
		print (agent)
		# 用正则来进行筛选,主要匹配MSIE 5~8
		result = re.findall("MSIE [567]",agent) 
		# print (result)
		if len(result)>0:
			# 如果浏览器是5~8版本，就显示升级页面
			# return render(request,"warning.html")
			path = (request.META['PATH_INFO'])
			print (path)
			print (path.find("/warning"))
			# 如果没找到信息，不在升级界面，就让它跳转
			if path.find("/warning") == -1:
				return redirect("/warning/")

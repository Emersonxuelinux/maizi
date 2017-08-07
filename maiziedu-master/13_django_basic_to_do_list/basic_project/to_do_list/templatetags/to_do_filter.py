from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from datetime import datetime
#声明标签库，方便后面的注册
register = template.Library()

# 定义一个过滤器用于去掉空格
# 可以用装饰器注册
@register.filter()
def cut_filter(value, arg):
	return value.replace(arg, '')


# 注册这个自定义过滤器，名字可以随便起，主要是指定调用哪个函数
# register.filter(name="cut_filter", filter_func=cut_filter)

@register.filter()
@stringfilter # 还可以用django内置过滤器自动转义为字符串

def lower(value):
	return value.lower()
# 装饰器写法就不需要指定调用哪个函数了
@register.filter(is_safe=True)
def add(value, arg):
	return mark_safe("%s %s" %(value, arg)) 

def mytimesince_filter(value):
	# 传入的value是信息发布时间时间
	# print (value)
	result = "刚刚"
	now = datetime.now()
	days = (now - value).days
	# print (days)
	if days // 30 != 0:
		result = str(days//30) + "月前"
	elif days // 7 !=0:
		result = str(days//7) + "周前"
	elif days != 0:
		result = str(days)+"天前"
	else:
		seconds = (now-value).seconds 
		if seconds//3600 !=0:
			result = str(seconds//3600) + "小时前"
		elif seconds//60 != 0:
			result = str(seconds//60)+"分钟前"
	return result
# 注册这个自定义过滤器，名字可以随便起，主要是指定调用哪个函数
register.filter("mytimesince",mytimesince_filter)

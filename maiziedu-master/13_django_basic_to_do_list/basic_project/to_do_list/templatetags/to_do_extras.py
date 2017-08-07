'''
模版是一个用django模版语言标记过的python字符串。模版可以包含模版标签和变量。
模版标签是在一个模版里起作用的标记。比如，一个模版标签可以产生控制结构的内容(if或者for)，可以获取数据库内容或者访问其它模版标签。
一个标签块被{%%}包围
变量标签被{{}}包围
context是一个传递给模版的key-value对。
模版渲染是通过从context获取值来替换模版中变量并执行所有的模版标签。

'''
from django import template
from datetime import datetime
from to_do_list.models import Item
import pdb
# 用来注册自定义标签
register = template.Library()


class AllenDateNode(template.Node):
	# 初始化日期格式
	def __init__(self, format_string,asvar):
		self.format_string = format_string
		self.asvar = asvar

	# 自定义标签主要就是实现这个函数
	def render(self,context):
		now = datetime.now().strftime(self.format_string)
        # 渲染时如果用了别名，就把这个值传给别名
		if self.asvar:
			context[self.asvar] = now
			return " "
		else:
			return now

# 创建编译函数，主要用于获取模板中的参数，并实例化相应的标签类


# 可以直接用装饰器注册，如果把name参数去掉，那就默认注册为函数名
@register.tag
def dateAllen(parse,token):
    args = token.split_contents()
    asvar = None
    # 如果参数长度为4，且倒数第二个是as，也就是说在模板中用自定义标签时用了这个字眼就会被识别
    if len(args) == 4 and args[-2] == "as":
        # 就自动把参数列表最后一个元素给标签的asvar属性
        asvar = args[-1]
    elif len(args) != 2:
        raise  template.TemplateSyntaxError("invalid agrs")
    return AllenDateNode(args[1][1:-1], asvar)

# Django自动有提供赋值装饰器
@register.assignment_tag()
def get_current_time(format_string):
	return datetime.now().strftime(format_string)

# 包含标签，指定渲染给某个模板，然后在引用这个标签的地方把数据和模板格式一起传入
@register.inclusion_tag("inclusion.html")
def things_is_done(done):
	things = Item.objects.filter(is_done=done)
	# pdb.set_trace()
	return {"things":things}
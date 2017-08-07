from jinja2 import Environment
from to_do_list.templatetags.to_do_filter import lower

def environment(**options):
    env = Environment(**options)
    # 在jinjia2中加入自定义过滤器，类似于django中的注册
    env.filters['allen_lower'] = lower
    return env

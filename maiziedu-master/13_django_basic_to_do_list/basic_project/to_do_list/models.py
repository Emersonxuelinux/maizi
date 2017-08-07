# coding:utf-8
from django.db import models

# Create your models here.
# 这个自定义的管理器就把一些数据操作直接包装在里面了，所以管理器其实就是用来包装复杂的数据处理
# 可以把多个相关操作封装在一个主题的管理器中
class TodoManager(models.Manager):
    def incomplete(self):
        return self.filter(is_done=False)

class TodoQuerySet(models.QuerySet):
    def incomplete(self):
        return self.filter(is_done=False)

class NewTodoManager(models.Manager):
    def get_querset(self):
        return TodoQuerySet(self.modle,using=self._db)

class Item(models.Model):
    content = models.CharField(max_length=100,verbose_name=u"待办事项")
    is_done = models.BooleanField(default=False,verbose_name=u"事项状态")
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name=u"发布时间")
    #指定后台看到的信息
    class Meta:
        verbose_name = '待办事项'
        verbose_name_plural = verbose_name
    #python3用这个返回信息，python2用__unicode__
    def __str__(self):
        return self.content
    # 另外指定Manager管理器，可以有多个
    todoList = models.Manager()
    # 具体调用形式就变成了Item.objects.all.incomplete()
    objects = NewTodoManager()

from django.db import models

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100,verbose_name='搜索记录')

    class Meta:
        verbose_name = u'搜索记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

'''
作者模型：一个作者有姓名。
作者详情模型：把作者的详情放到详情表，包含性别、email
地址和出生日期，作者详情模型和作者模型之间是一对一的关系（OneToOneField）
出版商模型：出版商有名称，地址，所在城市、省，国家，网站。
书籍模型：书籍有书名和出版日期。
一本书可能会有多个作者，一个作者也可以写多本书，所以作者和书籍的关系是多对多的关联关系[many-to-many]，
一本书只应该由一个出版商出版，所以出版商和书籍是一对多的关联关系[one-to-many]，也被称作外键[ForeignKey]。
'''
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30,verbose_name="名称")
    address = models.CharField(max_length=50,verbose_name="地址")
    city = models.CharField(max_length=60,verbose_name="城市")
    state_province = models.CharField(max_length=30,verbose_name="省份")
    country = models.CharField(max_length=50,verbose_name="国家")
    website = models.URLField(verbose_name="网址")

    class Meta:
        verbose_name = '出版商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
class Author(models.Model):
    name = models.CharField(max_length=30,verbose_name="姓名")

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
class AuthorDetail(models.Model):
    sex = models.BooleanField(max_length=1, choices=((0, '男'),(1,
                                                                 '女'),),verbose_name="性别")
    email = models.EmailField(verbose_name="邮箱")
    address = models.CharField(max_length=50,verbose_name="地址")
    birthday = models.DateField(verbose_name="生日")
    author = models.OneToOneField(Author,verbose_name="作者")

    class Meta:
        verbose_name = '作者细节'
        verbose_name_plural = verbose_name

class Book(models.Model):
    title = models.CharField(max_length=100,verbose_name="书名")
    authors = models.ManyToManyField(Author,verbose_name="作者")
    publisher = models.ForeignKey(Publisher,verbose_name="出版社")
    publication_date = models.DateField(verbose_name="出版日期")
    price = models.DecimalField(max_digits=5,decimal_places=2,default=10)
    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

from django.contrib import admin
from hello.models import *
# Register your models here.
admin.site.register(Author)
admin.site.register(AuthorDetail)
admin.site.register(Book)
admin.site.register(Publisher)

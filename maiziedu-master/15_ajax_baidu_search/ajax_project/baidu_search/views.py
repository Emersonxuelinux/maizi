# coding:utf-8
from django.shortcuts import render
from baidu_search.models import Item
from django.http import JsonResponse,HttpResponse
from django.core.serializers import serialize
import json
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    return render(request,'baidu_search_tutorial.html')
def autoComplete(request):
    query = request.GET.get('query',None)
    if query:
        item_list = Item.objects.filter(title__icontains=query)
    # 列表将会被转化为json数组
    return JsonResponse(item_list,safe=False)

def search(req):
    word = req.GET.get('word','')
    paginator = Paginator(Item.objects.filter(title__icontains=word),4)
    word_list = serialize('json',paginator.page(1))
    return HttpResponse(json.dumps(word_list),content_type='application/json')
  

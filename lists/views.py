from django.shortcuts import render,redirect
from django.http import HttpResponse

from lists.models import Item,List

# Create your views here.

def home_page(request):
    '''接收一个http请求，返回一个response'''
    return render(request,'home.html')

def view_list(req,list_id):
    list_ = List.objects.get(id=list_id)
    if req.method == "POST":
        Item.objects.create(text=req.POST["item_text"],list=list_)
    items = Item.objects.filter(list=list_)
    return render(req,'list.html',{
        "items":items,
    })

def new_list(req):
    list_ = List.objects.create()
    if req.method == "POST":
        Item.objects.create(text=req.POST['item_text'],list=list_)
    return redirect(f'/lists/{list_.id}')
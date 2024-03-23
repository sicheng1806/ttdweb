from django.shortcuts import render,redirect
from django.http import HttpResponse

from lists.models import Item

# Create your views here.

def home_page(request):
    '''接收一个http请求，返回一个response'''
    return render(request,'home.html')

def view_list(req):
    if req.method =="POST":
        Item.objects.create(text=req.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world')
    items = Item.objects.all()
    return render(req,'list.html',{
        "items":items,
    })

def new_list(req):
    if req.method == "POST":
        Item.objects.create(text=req.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world')
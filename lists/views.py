from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from django.http import HttpRequest

from lists.models import Item,List
from lists.forms import ItemForm

# Create your views here.

def home_page(request):
    '''接收一个http请求，返回一个response'''
    return render(request,'home.html',dict(form=ItemForm()))

def view_list(req:HttpRequest,list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if req.method == "POST":
        form = ItemForm(data=req.POST)
        if form.is_valid():
            form.save(list_)
            return redirect(list_)
    return render(req,'list.html',{"form":form,'list':list_})

def new_list(req:HttpRequest):
    form = ItemForm(data=req.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(list_)
        return redirect(list_)
    else:
        return render(req,'home.html',{"form":form})

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError


from lists.models import Item,List
from lists.forms import ItemForm

# Create your views here.

def home_page(request):
    '''接收一个http请求，返回一个response'''
    return render(request,'home.html',dict(form=ItemForm()))

def view_list(req,list_id):
    list_ = List.objects.get(id=list_id)
    if req.method == "POST":
        item = Item.objects.create(text=req.POST["item_text"],list=list_)
        try:
            item.full_clean()
        except ValidationError:
            item.delete()
        return redirect(list_)
    return render(req,'list.html',{'list':list_})

def new_list(req):
    list_ = List.objects.create()
    if req.method == "POST":
        item = Item.objects.create(text=req.POST['item_text'],list=list_)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            list_.delete()
            error = "You can't have an empty list item"
            return render(req,'home.html',dict(error=error))
    return redirect(list_)

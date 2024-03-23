from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    '''接收一个http请求，返回一个response'''
    new_item_text = request.POST.get('item_text','')
    if new_item_text:
        new_item_text = '1: ' + new_item_text
    return render(request,'home.html',{
        'new_item_text': new_item_text
    })
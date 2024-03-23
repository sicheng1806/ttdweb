from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    '''接收一个http请求，返回一个response'''
    return HttpResponse('<html><title>To-Do lists</title></html>')
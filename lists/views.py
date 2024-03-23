from django.shortcuts import render


# Create your views here.

def home_page(request):
    '''接收一个http请求，返回一个response'''
    return render(request,'home.html')
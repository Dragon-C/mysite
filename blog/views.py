from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from .models import Post

# Create your views here.

def index2(request):
    return render(request, 'blog/index2.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
        })

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',{'post_list':post_list})
    # return HttpResponse("aaaaa")

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'blog/detail.html',{'post':post})
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.utils.text import slugify

import markdown
from markdown.extensions.toc import TocExtension
import re

from .models import Post,visitCount

# Create your views here.

def get_count():
    visit_Count = visitCount.objects.get(id=1)
    co = visit_Count.count+1
    visit_Count.count = co
    visit_Count.save()

    return co

# def base(request,url):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request,url,{'post_list':post_list,'count':get_count()})


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
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),

        ]
    )
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    post.toc = m.group(1) if m is not None else ''

    # post_list = Post.objects.all().order_by('-created_time')[:5]

    return render(request, 'blog/detail.html',{'post':post})


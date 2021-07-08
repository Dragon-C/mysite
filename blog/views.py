from django.db.models.query_utils import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import HttpResponse
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib import messages

import markdown
from markdown.extensions.toc import TocExtension
import re

from .models import Post,visitCount,Category,Tag

# Create your views here.

def get_count():
    visit_Count = visitCount.objects.get(id=1)
    # co = visit_Count.count+1
    # visit_Count.count = co
    

    return visit_Count.save()
    # return visit_Count.increase_counts

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
    # print(post_list)

    paginator = Paginator(post_list, 5) # 每页显示 25 个联系人

    page = request.GET.get('page')

    # 旧版Django
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     # 如果用户请求的页码号不是整数，显示第一页
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     # 如果用户请求的页码号超过了最大页码号，显示最后一页
    #     posts = paginator.page(paginator.num_pages)

    posts = paginator.get_page(page)

    return render(request,'blog/index.html',{'posts': posts})

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 5

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])

    post.increase_views()

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

# def archive(request,year,month):
#     post_list = Post.objects.filter(
#         created_time__year=year,
#         created_time__month=month
#     ).order_by('-created_time')
#     return render(request,'blog/index.html',{'post_list':post_list})

class ArchiveView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):

        return super(ArchiveView,self).get_queryset().filter(created_time__year=self.kwargs.get('year'),created_time__month=self.kwargs.get('month'))

# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(
#         category=cate
#     ).order_by('-created_time')
#     return render(request,'blog/index.html',{'post_list':post_list})

class CategoryView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

# def tag(request,pk):
#     t = get_object_or_404(Tag,pk=pk)
#     post_list = Post.objects.filter(
#         tags=t
#     ).order_by('-created_time')
#     return render(request,'blog/index.html',{'post_list':post_list})

class TagView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        t = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=t)


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入关键词"
        messages.add_message(request,messages.ERROR,error_msg,extra_tags='danger')
        return redirect('blog:index')

    posts = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request,'blog/index.html',{'posts':posts})

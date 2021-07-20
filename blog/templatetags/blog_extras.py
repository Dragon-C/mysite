from django import template
from django.db.models.aggregates import Count

from django.utils import timezone
from datetime import datetime, timedelta

from ..models import Post, Category, Tag, visitCount, viewIP


register = template.Library()

@register.inclusion_tag("blog/inclusions/_recent_posts.html", takes_context=True)
def show_recent_posts(context, num=5):
    # request = context.get("request")
    
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
        
    }

@register.inclusion_tag("blog/inclusions/_archives.html", takes_context=True)
def show_archives(context):
    # request = context.get("request")
    
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC')
        
    }

@register.inclusion_tag("blog/inclusions/_categories.html", takes_context=True)
def show_categories(context):
    # request = context.get("request")
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
        
    }

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }

@register.inclusion_tag('blog/inclusions/_topcates.html', takes_context=True)
def top_cates(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
        
    }


# @register.inclusion_tag('blog/inclusions/_indexCount.html', takes_context=True)
# def get_counts(context):
#     # request = context.get("request")
    
#     return {
#         'count': visitCount.objects.get(id=1),
        
#     }


@register.inclusion_tag('blog/inclusions/_indexCount.html', takes_context=True)
def get_counts(context):
    request = context.get("request")

    recount_interval = 3600   # 单个IP重新计算浏览量的间隔时间
    del_interval = 86400       # 清除表中旧IP的间隔时间
    now_time = timezone.now()
    count = 0

    # if 'HTTP_X_FORWARDED_FOR' in request.META:        # 获取用户真实IP地址
    #     user_ip = request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     user_ip = request.META['REMOTE_ADDR']

    user_ip = request.META['HTTP_USER_AGENT']

    
    print('user_ip',user_ip)

    request_meta = request.META
    for k, v in request_meta.items():
        print(k,v)

    if viewIP.objects.filter(ip=user_ip).exists():             # 检查目前浏览的IP是否在表中存在
        obj = viewIP.objects.filter(ip=user_ip).first()
        old_time = viewIP.objects.filter(ip=user_ip).values('view_time')[0]['view_time']
        print(old_time)
        obj.view_time = now_time
        obj.save()
        if (now_time - old_time).seconds > recount_interval:   # IP存在，更新访问时间; 若距上次访问超过一小时，增加访问量                                                 # I
            count = 1
    else:                                                      # IP不存在，增加记录，增加访问量
        count = 1
        viewIP.objects.create(ip=user_ip,view_time=now_time)


    last_time = viewIP.objects.all().order_by('view_time').values('view_time')[0]['view_time']    # 获取IP表最早一条记录的时间
    if (now_time - last_time).seconds > del_interval:
        due_time = now_time - timedelta(seconds=recount_interval)                                 # 距现时间大于一定间隔时，算出时限，把比这个时限早的记录删除
        viewIP.objects.filter(view_time__lt=due_time).delete()

    if count:
        return {
            'count': visitCount.objects.get(id=1).save(),
            
        }
    else:
         return {
            'count': visitCount.objects.get(id=1),
            
        }       


from blog.models import Post
from .forms import CommentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from django.utils.text import slugify

import markdown
from markdown.extensions.toc import TocExtension
import re

# Create your views here.

@require_POST
def comment(request, post_pk):

    post = get_object_or_404(Post,pk=post_pk)

    form = CommentForm(request.POST)



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


    if form.is_valid():

        comment = form.save(commit=False)

        comment.post = post

        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')

        return redirect(post)

    context = {
        'post' : post,
        'form' : form,
        'failMark' : 1,
    }

    messages.add_message(request, messages.ERROR, '评论发表失败，请检查重试...', extra_tags='danger')

    # return render(request, 'comments/preview.html', context=context)
    return render(request, 'blog/detail.html', context=context)
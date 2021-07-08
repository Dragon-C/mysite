from django.contrib import admin
from django.apps import AppConfig
from .models import Comment

# Register your models here.

class CommentsConfig(AppConfig):
    name = 'comments'
    verbose_name = '评论'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','url','post','created_time']
    fields = ['name','email','url','post']

admin.site.register(Comment,CommentAdmin)
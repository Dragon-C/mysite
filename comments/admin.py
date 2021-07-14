from django.contrib import admin
from django.apps import AppConfig
from .models import Comment

# Register your models here.

class CommentsConfig(AppConfig):
    name = 'comments'
    verbose_name = '评论'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','url','post','created_time','text']
    fields = ['name','email','url','post','text']

admin.site.register(Comment,CommentAdmin)
from django import urls
from django.urls import re_path, path, include
from django.conf import settings
from django.conf.urls.static import static

from .import views
app_name='blog'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    path('a', views.index2, name='index2'),
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category'),
    path("tag/<int:pk>", views.TagView.as_view(), name='tag'),
    path("search/", views.search, name='search'),
    path("about/", views.AboutView.as_view(), name='about'),

]



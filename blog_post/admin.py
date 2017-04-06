#coding:utf-8
from django.contrib import admin

from blog_post.models import Article, Category, BlogComment

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(BlogComment)
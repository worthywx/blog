#coding:utf-8
from django.contrib import admin

from blog_post.models import Article, Category, BlogComment

class ArticleAdmin(admin.ModelAdmin):
	search_fields = ('title', 'body')
	date_hierarchy = 'create_time'
	fields = ('title', 'abstract', 'body',  'img', 'category')



admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(BlogComment)
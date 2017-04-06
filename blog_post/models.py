# -*- coding: UTF-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

class Article(models.Model):
	title = models.CharField('标题', max_length=70)
	abstract = models.TextField('摘要', default='abstract')
	body = models.TextField('正文')
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	last_modified_time = models.DateTimeField('修改时间', auto_now=True)
	views = models.PositiveIntegerField('浏览量', default=0)
	category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.title
		
	class Meta:
		ordering = ['-last_modified_time']
		
	def get_absolute_url(self):
		return reverse('blog_post:detail', kwargs={'article_id': self.pk})
		
class Category(models.Model):
	name = models.CharField('类名', max_length=20)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	last_modified_time = models.DateTimeField('修改时间', auto_now=True)
	
	def __str__(self):
		return self.name
		
class BlogComment(models.Model):
    user_name = models.CharField('评论者名字', max_length=100)
    user_email = models.EmailField('评论者邮箱', max_length=255)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]


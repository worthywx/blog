#coding:utf-8
from django.shortcuts import render, get_object_or_404,HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from blog_post.models import Article, Category, BlogComment
import markdown2
from .forms import BlogCommentForm
from django.db.models import Count
	
class IndexView(ListView):
	template_name = "index.html"
	context_object_name = "article_list"
	
	def get_queryset(self):
		article_list = Article.objects.all()
		for article in article_list:
			article.abstract = markdown2.markdown(article.abstract, )
		return article_list
		
	def get_context_data(self, **kwargs):
		kwargs['category_list'] = Category.objects.annotate(article_total=Count('article')).order_by('name')
		kwargs['comment_list_all'] = BlogComment.objects.select_related().all()[0:5]
		kwargs['archive_list'] = []
		archive_list = Article.objects.datetimes("create_time", "month")
		for archive in archive_list:
			list_temp = {}
			list_temp['archive'] = archive.strftime("%Y-%m")
			list_temp['number'] = len(Article.objects.filter(create_time__icontains=list_temp['archive']))
			kwargs['archive_list'].append(list_temp)
		return super(IndexView, self).get_context_data(**kwargs)
		
class ArticleDetailView(DetailView):
	model = Article
	template_name = "blog_post.html"
	context_object_name = "article"
	pk_url_kwarg = "article_id"

	def get_object(self):
		obj = super(ArticleDetailView, self).get_object()
		obj.views = obj.views + 1
		obj.save()
		obj.body = markdown2.markdown(obj.body)
		next_article = Article.objects.filter(id__lt=obj.id).order_by('-create_time')
		prev_article = Article.objects.filter(id__gt=obj.id).order_by('create_time')
		if len(next_article) == 0:
			obj.next = 0
		else:
			obj.next = 1
			obj.next_title = next_article[0].title
			obj.next_id = next_article[0].id
			
		if len(prev_article) == 0:
			obj.prev = 0
		else:
			obj.prev = 1
			obj.prev_title = prev_article[0].title
			obj.prev_id = prev_article[0].id
			
		return obj
	
	def get_context_data(self, **kwargs):
		kwargs['comment_list'] = self.object.blogcomment_set.all()
		kwargs['category_list'] = Category.objects.annotate(article_total=Count('article')).order_by('name')
		kwargs['comment_list_all'] = BlogComment.objects.select_related().all()[0:5]
		kwargs['form'] = BlogCommentForm()
		kwargs['archive_list'] = []
		archive_list = Article.objects.datetimes("create_time", "month")
		for archive in archive_list:
			list_temp = {}
			list_temp['archive'] = archive.strftime("%Y-%m")
			list_temp['number'] = len(Article.objects.filter(create_time__icontains=list_temp['archive']))
			kwargs['archive_list'].append(list_temp)
		return super(ArticleDetailView, self).get_context_data(**kwargs)
		
class CategoryView(IndexView):
	template_name = "index.html"
	context_object_name = "article_list"
	def get_queryset(self):
		article_list = Article.objects.filter(category_id=self.kwargs['cate_id'])
		for article in article_list:
			article.abstract = markdown2.markdown(article.abstract,)
		return article_list
		
class CommentPostView(FormView):
    form_class = BlogCommentForm
    template_name = 'blog_post.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)
		
class ArchiveView(IndexView):
	template_name = "index.html"
	context_object_name = "article_list"
	def get_queryset(self):
		article_list = Article.objects.filter(create_time__icontains=self.kwargs['archive_time'])
		for article in article_list:
			article.abstract = markdown2.markdown(article.abstract,)
		return article_list
	
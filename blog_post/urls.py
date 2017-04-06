from django.conf.urls import url
from blog_post import views
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^blog/article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
	url(r'^blog/category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
	url(r'^comment/article/(?P<article_id>[0-9]+)$', views.CommentPostView.as_view(), name='comment'),
	url(r'^blog/archive/(?P<archive_time>\d\d\d\d-\d\d)/$', views.ArchiveView.as_view(), name='archive'),
]
from django.conf.urls import url
from .views import (
    AllArticlesAPIView,
    ArticleDetailAPIView,
    ArticlesByCategoryAPIView,
)

urlpatterns = [
    url(r'^$', AllArticlesAPIView.as_view(), name='list_api'),
    url(r'^article/(?P<slug>[\w-]+)/$', ArticleDetailAPIView.as_view(), name='detail_api'),
    url(r'^category/(?P<category>[a-zA-Z0-9].*)/$', ArticlesByCategoryAPIView.as_view(), name='category_api'),
]

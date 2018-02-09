from django.conf.urls import url
from .views import (
    AllArticlesAPIView,
    # LoginAPIView,
)

urlpatterns = [
    url(r'^$', AllArticlesAPIView.as_view(), name='list_api'),
    # url(r'^article/(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='detail'),
    # url(r'^category/(?P<category>[a-zA-Z0-9].*)/$', ArticlesByCategoryListView.as_view(), name='category'),
]

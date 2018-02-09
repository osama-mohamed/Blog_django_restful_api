from django.conf.urls import url
from .views import (
    CommentThreadView,
    CommentDeleteView,
)


urlpatterns = [
    url(r'^(?P<id>\d+)/$', CommentThreadView.as_view(), name='thread'),
    url(r'^(?P<id>\d+)/delete/$', CommentDeleteView.as_view(), name='delete'),
]

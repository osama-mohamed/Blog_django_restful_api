from django.conf.urls import url
from .views import (
    AddCommentAPIView,
)

urlpatterns = [
    url(r'^add_comment/(?P<id>\d+)/$', AddCommentAPIView.as_view(), name='add_api'),
    # url(r'^(?P<id>\d+)/$', CommentThreadView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', CommentDeleteView.as_view(), name='delete'),
]

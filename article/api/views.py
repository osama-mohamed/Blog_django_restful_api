from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .serializers import (
    AllArticlesSerializer,
    ArticleDetailSerializer,
)
from .pagination import ArticlePageNumberPagination
from article.models import Article
from comment.models import Comment
from comment.api.serializers import CommentThreadReplySerializer

User = get_user_model()


class AllArticlesAPIView(ListAPIView):
    serializer_class = AllArticlesSerializer
    pagination_class = ArticlePageNumberPagination
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.filter(publish=True).order_by('-id')
        query = self.request.GET.get('search')
        if query:
            queryset = Article.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(category__category__icontains=query)
            ).distinct().order_by('-id')
        return queryset


class ArticleDetailAPIView(RetrieveAPIView):
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.filter(slug__iexact=self.kwargs['slug'], publish=True)
        article = queryset.first()
        article.number_of_views += 1
        article.save()
        return queryset


class ArticlesByCategoryAPIView(ListAPIView):
    serializer_class = AllArticlesSerializer
    pagination_class = ArticlePageNumberPagination
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.filter(
            category__category=self.kwargs['category'],
            publish=True
        ).order_by('-id')
        return queryset

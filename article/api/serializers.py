from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedIdentityField,
)
from django.core.urlresolvers import reverse
from django.conf import settings

from article.models import Article
from comment.models import Comment
from comment.api.serializers import ArticleCommentSerializer


class AllArticlesSerializer(ModelSerializer):
    category = SerializerMethodField(read_only=True)
    detail_url = HyperlinkedIdentityField(
        view_name='articles_api:detail_api',
        lookup_field='slug'
    )
    category_url = HyperlinkedIdentityField(
        view_name='articles_api:category_api',
        lookup_field='category'
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'detail_url',
            'category_url',
            'category',
            'title',
            'body',
            'number_of_views',
            'read_time',
            'image',
            'slug',
            'publish',
            'block_comment',
            'added',
            'updated',
        ]

    def get_category(self, obj):
        return str(obj.category)


class ArticleDetailSerializer(ModelSerializer):
    category = SerializerMethodField(read_only=True)
    all_products_url = SerializerMethodField()
    add_comment_url = HyperlinkedIdentityField(
        view_name='comments_api:add_api',
        lookup_field='id'
    )
    count_comments = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id',
            'all_products_url',
            'category',
            'title',
            'body',
            'number_of_views',
            'read_time',
            'image',
            'slug',
            'publish',
            'block_comment',
            'added',
            'updated',
            'add_comment_url',
            'count_comments',
            'comments',
        ]

    def get_category(self, obj):
        return str(obj.category)

    def get_all_products_url(self, obj):
        return settings.BASE_URL + reverse('articles_api:list_api')

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_by_queryset(obj)
        comments = ArticleCommentSerializer(comments_qs, many=True).data
        return comments

    def get_count_comments(self, obj):
        comments_qs = Comment.objects.filter_by_queryset(obj)
        comments = len(comments_qs)
        return comments


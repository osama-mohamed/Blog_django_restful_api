from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
    SerializerMethodField,
    HyperlinkedIdentityField,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.conf import settings

from article.models import Article

User = get_user_model()


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
        ]

    def get_category(self, obj):
        return str(obj.category)

    def get_all_products_url(self, obj):
        return settings.BASE_URL + reverse('articles_api:list_api')

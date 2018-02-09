from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
    SerializerMethodField,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q

from article.models import Article

User = get_user_model()


class AllArticlesSerializer(ModelSerializer):
    category = SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
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

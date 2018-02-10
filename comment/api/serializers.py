from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
)
from django.core.urlresolvers import reverse
from django.conf import settings

from comment.models import Comment


class ArticleCommentSerializer(ModelSerializer):
    content = CharField(label='Comment')
    thread_url = SerializerMethodField()
    delete_url = SerializerMethodField()
    replies_count = SerializerMethodField()
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'content',
            'thread_url',
            'delete_url',
            'replies_count',
            'replies',
        ]

    def get_thread_url(self, obj):
        return str(settings.BASE_URL + reverse('comments_api:thread_api', kwargs={'id': obj.id}))

    def get_delete_url(self, obj):
        return str(settings.BASE_URL + reverse('comments_api:delete_api', kwargs={'id': obj.id}))

    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentThreadSerializer(obj.children(), many=True).data
        return None


class CommentSerializer(ModelSerializer):
    content = CharField(label='Comment')

    class Meta:
        model = Comment
        fields = [
            'parent',
            'content',
        ]


class CommentThreadSerializer(ModelSerializer):
    content = CharField(label='Comment')
    replies_count = SerializerMethodField()
    replies = SerializerMethodField()
    delete_url = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'content',
            'delete_url',
            'replies_count',
            'replies',
        ]

    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentThreadSerializer(obj.children(), many=True).data
        return None

    def get_delete_url(self, obj):
        return str(settings.BASE_URL + reverse('comments_api:delete_api', kwargs={'id': obj.id}))


class CommentThreadReplySerializer(ModelSerializer):
    content = CharField(label='Comment')

    class Meta:
        model = Comment
        fields = [
            'content',
        ]

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
)
from comment.models import Comment


class CommentSerializer(ModelSerializer):
    content = CharField(label='Comment')

    class Meta:
        model = Comment
        fields = [
            'parent',
            'content',
        ]

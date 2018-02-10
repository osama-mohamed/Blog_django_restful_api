from rest_framework.generics import (
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType

from .serializers import (
    CommentSerializer,
    CommentThreadSerializer,
    CommentThreadReplySerializer,
)
from .permissions import IsOwnerOrReadOnly
from article.models import Article
from comment.models import Comment


class AddCommentAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = self.request.user
        if user.is_authenticated:
            article = Article.objects.filter(id=id, publish=True).first()
            if article.block_comment is True:
                return Response(
                    {'message': ['This article is blocked for adding comments!']},
                    status=HTTP_400_BAD_REQUEST
                )
            if request.POST.get('content') == '' or request.POST.get('content') is None:
                return Response(
                    {'message': ['You must write a valid comment!']},
                    status=HTTP_400_BAD_REQUEST
                )
            else:
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid():
                    new_data = serializer.data
                    content_type = ContentType.objects.get(model='article')
                    parent_obj = None
                    try:
                        parent_id = int(new_data['parent'])
                    except:
                        parent_id = None
                    if parent_id:
                        parent_qs = Comment.objects.filter(id=parent_id)
                        if parent_qs.exists() and parent_qs.count() == 1:
                            parent_obj = parent_qs.first()
                    new_comment = Comment.objects.create(
                        user=self.request.user,
                        content_type=content_type,
                        object_id=id,
                        parent=parent_obj,
                        content=new_data['content'],
                    )
                    return Response(
                        {'message': ['Successfully added your comment!']},
                        status=HTTP_200_OK
                    )
        else:
            return Response(
                {'message': ['You do not have permission to do that!']},
                status=HTTP_400_BAD_REQUEST
            )


class CommentThreadAPIView(RetrieveAPIView):
    serializer_class = CommentThreadSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.filter(id=self.kwargs['id'])
        return queryset

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = self.request.user
        if user.is_authenticated:
            serializer = CommentThreadReplySerializer(data=request.data)
            if serializer.is_valid():
                new_data = serializer.data
                content_type = ContentType.objects.get(model='article')
                parent_obj = None
                parent_id = id
                if parent_id:
                    parent_qs = Comment.objects.filter(id=parent_id)
                    if parent_qs.exists() and parent_qs.count() == 1:
                        parent_obj = parent_qs.first()
                new_comment = Comment.objects.create(
                    user=self.request.user,
                    content_type=content_type,
                    object_id=id,
                    parent=parent_obj,
                    content=new_data['content'],
                )
                return Response(
                    {'message': ['Successfully added your comment!']},
                    status=HTTP_200_OK
                )
        else:
            return Response(
                {'message': ['You do not have permission to do that!']},
                status=HTTP_400_BAD_REQUEST
            )


class CommentDeleteAPIView(DestroyAPIView):
    serializer_class = CommentThreadSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.filter(id=self.kwargs['id'])
        return queryset

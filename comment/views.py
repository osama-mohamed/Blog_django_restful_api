from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import Comment
from .forms import CommentForm


class CommentThreadView(DetailView):
    template_name = 'comment/comment_thread.html'

    def get_object(self, **kwargs):
        id = self.kwargs['id']
        return get_object_or_404(Comment, id=id)

    def get_context_data(self, **kwargs):
        context = super(CommentThreadView, self).get_context_data(**kwargs)
        id = self.kwargs['id']
        comment = Comment.objects.filter(id=id).first()
        context['comment'] = comment
        initial_data = {
            'content_type': comment.content_type,
            'object_id': comment.object_id,
        }
        form = CommentForm(None, initial=initial_data)
        context['form'] = form
        return context

    def post(self, request, **kwargs):
        id = self.kwargs['id']
        comment = Comment.objects.filter(id=id).first()
        form = CommentForm(request.POST)
        if form.is_valid():
            c_type = form.cleaned_data.get('content_type')
            content_type = ContentType.objects.get(model=c_type)
            obj_id = form.cleaned_data.get('object_id')
            content_data = form.cleaned_data.get('content')
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()
            new_comment, created = Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=obj_id,
                content=content_data,
                parent=parent_obj
            )
            return HttpResponseRedirect(comment.get_absolute_url())


class CommentDeleteView(DetailView):
    template_name = 'comment/comment_delete.html'

    def get_object(self, **kwargs):
        id = self.kwargs['id']
        comment = Comment.objects.filter(id=id).first()
        return comment

    def post(self, request, **kwargs):
        id = self.kwargs['id']
        comment = Comment.objects.filter(id=id).first()
        comment.delete()
        return HttpResponseRedirect(comment.content_object.get_absolute_url())

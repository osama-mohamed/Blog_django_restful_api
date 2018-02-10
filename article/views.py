from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .models import Article, Category
from comment.models import Comment
from comment.forms import CommentForm


class AllArticlesListView(ListView):
    template_name = 'article/all_articles.html'
    queryset = Article.objects.all().order_by('-id')
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(AllArticlesListView, self).get_context_data(**kwargs)

        qs = Article.objects.all().order_by('-id')
        paginator = Paginator(qs, self.paginate_by)
        page_request = 'page'
        page = self.request.GET.get(page_request)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        context['objects'] = queryset
        context['page_request'] = page_request

        context['categories'] = Category.objects.all()
        return context

    def post(self, request):
        search = self.request.POST.get('search')
        if search == '':
            return redirect('articles:list')
        if search:
            queryset = Article.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search) |
                Q(category__category__icontains=search)
            ).distinct().order_by('-id')

            context = {
                'object_list': queryset,
                'categories': Category.objects.all(),
            }
            return render(request, 'article/all_articles.html', context)


class ArticleDetailView(DetailView):
    template_name = 'article/article_detail.html'

    def get_object(self, **kwargs):
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()
        article.number_of_views += 1
        article.save()
        return get_object_or_404(Article, slug=slug, publish=True)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()
        comments = article.comments
        context['comments'] = comments
        initial_data = {
            'content_type': article.get_content_type,
            'object_id': article.id,
        }
        form = CommentForm(None, initial=initial_data)
        context['form'] = form
        return context

    def post(self, request, **kwargs):
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()
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
            return redirect('articles:detail', slug=article.slug)


class ArticlesByCategoryListView(ListView):
    template_name = 'article/all_articles.html'
    paginate_by = 20

    def get_queryset(self):
        qs = Article.objects.filter(category__category=self.kwargs['category']).order_by('-id')
        return qs

    def get_context_data(self, **kwargs):
        context = super(ArticlesByCategoryListView, self).get_context_data(**kwargs)

        qs = Article.objects.filter(category__category=self.kwargs['category']).order_by('-id')
        paginator = Paginator(qs, self.paginate_by)
        page_request = 'page'
        page = self.request.GET.get(page_request)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        context['objects'] = queryset
        context['page_request'] = page_request

        context['categories'] = Category.objects.all()
        return context

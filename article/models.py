from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.models import ContentType

from .utils import create_slug, get_read_time
from comment.models import Comment


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    number_of_articles = models.IntegerField(default=0, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    def get_absolute_categories_url(self):
        return reverse('articles:category', kwargs={'category': self.category})

    class Meta:
        verbose_name_plural = 'Categories'


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    number_of_views = models.PositiveIntegerField(default=0, blank=True, null=True)
    read_time = models.IntegerField(default=0)
    image = models.ImageField()
    publish = models.BooleanField(default=True)
    block_comment = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    @property
    def comments(self):
        queryset = self
        comments = Comment.objects.filter_by_queryset(queryset)
        return comments

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def pre_save_article_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.body:
        html_string = instance.body
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


def post_save_article_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = Article.objects.filter(slug=instance)
        if qs.exists() and qs.count() == 1:
            article = qs.first()
            category = Category.objects.get(category=article.category)
            category.number_of_articles += 1
            category.save()


pre_save.connect(pre_save_article_reciver, sender=Article)
post_save.connect(post_save_article_receiver, sender=Article)

from django.utils.text import slugify
from django.utils.html import strip_tags
import math
import re


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    article = instance.__class__
    qs = article.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def count_words(html_string):
    word_string = strip_tags(html_string)    # remove html tags
    matching_words = re.findall(r'\w+', word_string)    # make list of words
    count = len(matching_words)    # count words in the list
    return count


def get_read_time(html_string):
    count = count_words(html_string)    # return of count_words function that count words in the list
    read_time_min = math.ceil(count / 200.0)    # div number of words / 200 word speed in one minute
    return int(read_time_min)

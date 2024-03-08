from django import template
from django.db.models import Count

from ..models import Bloginfo, Category, Tag

register = template.Library()


@register.simple_tag
def get_new_blogs():
    return Bloginfo.objects.all().order_by("-create_time")[:5]

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_blogs=Count('bloginfo')).filter(num_blogs__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_blogs=Count('bloginfo')).filter(num_blogs__gt=0)

@register.simple_tag
def get_arhcives():
    return Bloginfo.objects.dates('create_time', 'month', order='DESC')



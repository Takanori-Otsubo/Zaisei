from django import template
from mysite.models import Category, Post
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

register = template.Library()


@register.inclusion_tag('mysite/tags/category.html')
def render_category_links():
    categories = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))
    return {'category_list': categories}


@register.inclusion_tag('mysite/tags/date.html')
def render_post_links():
    dates = Post.objects.annotate(
        month=TruncMonth('published_at')).values('month').annotate(count=Count('pk')).order_by()
    return {'dates': dates}

from django import template

from ..models import Like

register = template.Library()


@register.simple_tag
def like_toggle(user, slug):
    return Like.like_toggle(user=user, slug=slug)

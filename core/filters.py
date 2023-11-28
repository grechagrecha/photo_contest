import django_filters

from .models import Post


class PostFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = [

        ]

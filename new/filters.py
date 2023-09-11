# from django_filters import FilterSet
# from .models import Post
#
#
# class PostFilter(FilterSet):
#     # model = Post
#
#    class Meta:
#        model = Post
#        fields = {
#            'title': ['icontains'],
#            'author__user__username': ['icontains'],
#            'post_time': ['gt'],
#        }


import django_filters.widgets
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter
from django_filters.widgets import DateRangeWidget

from .models import Post


#построение фильтров поиска
class PostFilter(FilterSet):
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )
    post_time = DateFromToRangeFilter(
        widget=DateRangeWidget(attrs={'placeholder': 'ГГГГ.ММ.ДД'}),
        lookup_expr='gt',
        label='За период'
    )
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    class Meta:
        model = Post
        fields = {'title'}



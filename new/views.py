from datetime import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from . import tasks
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category

logger = logging.getLogger('main')


#представление авторы
class AuthorList(ListView):
    model = Author
    context_object_name = 'Author'

#представление список постов
class PostsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    logger.info('Страница постов загружена!')


#представление поиск по статьям
class SearchPostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    # success_url = reverse_lazy('news_search')

    logger.info('Страница поиска постов загружена!')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

#представление детальное статьи
class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    logger.info('Страница поста загружена!')

#представление создании новости
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news')

    logger.info('Страница создание постов загружена!')

    # отправка письма при создании поста
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'PS'
        post.save()
        tasks.send_mail_subscriber.delay(post.pk)
        return super().form_valid(form)


    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.type = 'PS'
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


#представление редактирование новости
class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news')

    logger.info('Страница обновление постов загружена!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

#представление удаление новости
class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

#представление создание статьи
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    success_url = reverse_lazy('news')

    logger.info('Страница создание статьи загружена!')

    # отправка письма при создании поста
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        post.save()
        tasks.send_mail_subscriber.delay(post.pk)
        return super().form_valid(form)

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.type = 'AR'
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

#представление редактирование статьи
class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    logger.info('Страница обновление статьи загружена!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

#представление удаление статьи
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

#представление списка постов одной категории
class CategoryDetail(DetailView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'

    logger.info('Страница категории загружена!')

    def get_context_data(self, **kwargs):
        category = self.get_object()
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(post_category = category)
        context['is_not_subscriber'] = self.request.user not in category.subscribers.all()
        return context

#представление кнопок на подписку/отписку от категории постов
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписались.'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались.'
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})






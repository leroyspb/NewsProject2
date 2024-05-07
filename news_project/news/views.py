from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import OuterRef, Exists
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import NewsFilter
from .forms import NewsForm
from .models import Post, Subscription, Category
from datetime import datetime


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = '-creation_time_in'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
# Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — post_detail.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class SearchNews(ListView):

    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = '-creation_time_in'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        if self.request.GET:
            return self.filterset.qs
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = NewsForm

    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news_create/':
            post.post.news = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article/articles_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles_create/':
            post.post.news = 'AR'
        return super().form_valid(form)


# Добавляем представление для изменения товара.
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news/post_create.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'article/articles_create.html'


# Представление удаляющее пост или статью.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('post')

    def get_success_url(self):
        return reverse_lazy('news')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article/article_delete.html'
    success_url = reverse_lazy('post')

    def get_success_url(self):
        return reverse_lazy('news')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
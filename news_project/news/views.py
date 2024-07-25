from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import OuterRef, Exists
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache  # импортируем наш кэш
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .tasks import send_email_new_post
from .filters import NewsFilter
from .forms import NewsForm
from .models import Post, Subscription, Category
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext as _  # импортируем функцию для перевода
import pytz  # импортируем стандартный модуль для работы с часовыми поясами

from .translation import PostTranslationOptions, CategoryTranslationOptions


class Index(View):
    def get(self, request):

        models = PostTranslationOptions, CategoryTranslationOptions

        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))
        # по пост-запросу будем добавлять в сессию часовой пояс,
        # который и будет обрабатываться написанным нами ранее middleware

    # def post(self, request):
    #     request.session['django_timezone'] = request.POST['timezone']
    #     return redirect('/')


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = '-creation_time_in'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем обычный запрос
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
    queryset = Post.objects.all()


def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
    obj = cache.get(f'news-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует так же.
    # Он забирает значение по ключу, если его нет, то забирает None
    # если объекта нет в кэше, то получаем его и записываем в кэш
    if not obj:
        obj = super().get_object(queryset=self.queryset)
        cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj


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


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('post_create',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = NewsForm

    # модель
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/post_create.html'

    # def form_valid(self, form):
    #     form.instance.type = 'NW'
    #     form.instance.author = self.request.user.author
    #     self.object = form.save()
    #     # Сохранить публикацию, чтобы у нее был идентификатор.
    #     form.save(commit=False)
    #     form.save_m2m()  # Сохранение данных «многие ко многим»
    #     return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()


    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news_create/':
            post.post.news = 'NW'
        post.save()
        send_email_new_post.delay(post.pk)
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article/articles_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles_create/':
            post.post.news = 'AR'
        post.save()
        send_email_new_post.delay(post.pk)
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


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


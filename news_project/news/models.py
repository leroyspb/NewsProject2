from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext_lazy as gettext


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=gettext('enter the author name'))  # добавим переводящийся текст подсказку к полю))
    rating = models.IntegerField(default=0, help_text=gettext('enter your rating here'))

    def __str__(self):
        return self.user.username

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum("rating"), 0))["pr"]
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum("rating"), 0))["cr"]
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum("rating"), 0))["pcr"]

        print(f'Рейтинг за статьи и новости: {posts_rating}')
        print('--------------')
        print(f'Рейтинг за комментарии: {comments_rating}')
        print('--------------')
        print(f'Рейтинг комментариев к статье и новости: {posts_comments_rating}')

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, help_text=gettext('Category name'))  # добавим переводящийся текст подсказку к полю)
    subscribers = models.ManyToManyField(User, related_name='categories', through='Subscription')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=gettext('author post'))

    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_PAPER = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новости'))

    categoryType = models.CharField(max_length=2, choices=CATEGORY_PAPER, default=ARTICLE)
    creation_time_in = models.DateTimeField(auto_now_add=True, verbose_name=gettext('date published'))
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name=gettext('category post'))
    title = models.CharField(max_length=128, verbose_name=gettext('title'))
    text = models.TextField(verbose_name=gettext('text post'))
    rating = models.IntegerField(default=0, help_text=gettext('The rating is indicated here'))
    related_name = 'posts',

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        # return '{}'.format(self.title)
        return f'{self.title}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу
        return reverse('post', kwargs={'pk': self.pk})
    # return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.comment_post.author.user.username + '---' + str(self.id)


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

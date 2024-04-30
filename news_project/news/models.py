from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

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
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_PAPER = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новости'))

    categoryType = models.CharField(max_length=2, choices=CATEGORY_PAPER, default=ARTICLE)
    creation_time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

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
        return reverse('post', args=[str(self.id)])

        # return reverse('post', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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

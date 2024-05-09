from django.urls import path
# Импортируем созданное нами представление
from .views import *

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,

   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/', PostList.as_view(), name='news'),
   path('news/<int:pk>/', PostDetail.as_view(), name='post'),
   path('news/search/', SearchNews.as_view(), name='search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/edit', ArticleUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list')

]

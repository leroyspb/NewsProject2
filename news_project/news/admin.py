from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'author', 'categoryType', 'rating') # оставляем только имя и цену товара
    list_filter = ('rating', 'author', 'title') # добавляем примитивные фильтры в нашу админку
    fields = ['author', 'title', 'text', 'categoryType']
    search_fields = ('title', 'categoryType') # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Post, ProductAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)



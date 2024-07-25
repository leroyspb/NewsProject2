from django.contrib import admin
from .models import Post, Category, PostCategory, Author
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin):
    model = Post


class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Author)



from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'text', 'categoryType']
    list_display = ('title', 'author', 'categoryType', 'rating')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)



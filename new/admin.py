from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment

#добавление моделей в админ панель
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)


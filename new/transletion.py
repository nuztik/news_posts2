from .models import Category, Post, Comment
from modeltranslation.translator import register, TranslationOptions


# регистрируем наши модели для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name')  # указываем, какие именно поля надо переводить в виде кортежа


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('content')
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Review, FAQ, ArticleCategory, Article, FAQCategory, Client


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'user_tag', 'user_photo', 'short_text']

    def short_text(self, obj):
        return obj.text[:20] + '...'

    short_text.short_description = 'Текст'


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_question', 'short_answer', 'home_page', 'business_page', 'str_categories']

    def str_categories(self, obj):
        return ', '.join([cat.name for cat in obj.categories.all()])

    def short_question(self, obj):
        return obj.question[:20] + '...'

    def short_answer(self, obj):
        return obj.answer[:20] + '...'

    short_question.short_description = 'Вопрос'
    short_answer.short_description = 'Ответ'


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ['id', 'title', 'second_title', 'str_categories', 'short_text']
    summernote_fields = ('text',)

    def str_categories(self, obj):
        return ', '.join([cat.name for cat in obj.categories.all()])

    def short_text(self, obj):
        return obj.text[:20] + '...'

    short_text.short_description = 'Вопрос'
    str_categories.short_description = 'Категории'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']

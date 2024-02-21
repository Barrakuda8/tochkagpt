from django.contrib import admin
from .models import Message, Attachment, SampleCategory, Sample, Tariff, Subscription, Chat, UserSample, \
    UserSamplesLikes, NewChatCategory, NewChatSample, NewChatInstruction


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'requests_GPT35', 'requests_GPT4', 'requests_SD', 'requests_MJ',
                    'requests_DL3', 'samples_included', 'most_chosen']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tariff', 'start_date', 'end_date']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_current', 'is_deleted']

    def save_model(self, request, obj, form, change):
        if not change or (change and 'is_current' in form.changed_data):
            if obj.is_current:
                current = Chat.objects.filter(user__pk=obj.user.pk, is_current=True)
                if current.exists():
                    current = current.first()
                    current.is_current = False
                    current.save()
            else:
                obj.is_current = True
        print(form.changed_data)
        return super(ChatAdmin, self).save_model(request, obj, form, change)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'chat', 'is_sender', 'used_ai', 'short_text', 'is_deleted']

    def short_text(self, obj):
        return obj.text[:20] + '...'

    short_text.short_description = 'Текст'


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Attachment._meta.get_fields()]


@admin.register(SampleCategory)
class SampleCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_description', 'str_categories']

    def str_categories(self, obj):
        return ', '.join([cat.name for cat in obj.categories.all()])

    def short_description(self, obj):
        return obj.description[:20] + '...'

    short_description.short_description = 'Вопрос'
    str_categories.short_description = 'Категории'


@admin.register(UserSample)
class UserSampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'short_description', 'str_categories']

    def str_categories(self, obj):
        return ', '.join([cat.name for cat in obj.categories.all()])

    def short_description(self, obj):
        return obj.description[:20] + '...'

    short_description.short_description = 'Вопрос'
    str_categories.short_description = 'Категории'


@admin.register(UserSamplesLikes)
class UserSamplesLikesCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sample']


@admin.register(NewChatCategory)
class NewChatCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'section']


@admin.register(NewChatSample)
class NewChatSampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'section', 'category']


@admin.register(NewChatInstruction)
class NewChatInstructionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']

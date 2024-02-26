import re
from datetime import datetime
import pytz
from django.db import models
from django.dispatch import receiver

from authentication.models import User
from tochkagpt import settings


class Tariff(models.Model):

    name = models.CharField(max_length=32, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена (руб/мес)')
    characteristics = models.JSONField(default=dict, verbose_name='Характеристики ({"details": []})')
    requests_GPT35 = models.PositiveIntegerField(default=0, verbose_name='Количество запросов в месяц (GPT-3.5)')
    requests_GPT4 = models.PositiveIntegerField(default=0, verbose_name='Количество запросов в месяц (GPT-4)')
    requests_VS = models.PositiveIntegerField(default=0, verbose_name='Количество запросов в месяц (Vision)')
    requests_SD = models.PositiveIntegerField(default=0, verbose_name='Количество запросов в месяц (Stable Diffusion)')
    requests_MJ = models.PositiveIntegerField(default=0, verbose_name='Количество запросов в месяц (Midjourney)')
    requests_DL3 = models.PositiveIntegerField(default=0, verbose_name='Количество запросов в месяц (Dall-e 3)')
    samples_included = models.BooleanField(default=False, verbose_name='Подключены шаблоны')
    most_chosen = models.BooleanField(default=False, verbose_name='Самый часто выбираемый')

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name

    @property
    def get_characteristics(self):
        result = []
        data = {
            'GPT35': 'запросов GPT-3.5',
            'GPT4': 'запросов GPT-4',
            'VS': 'запросов Vision',
            'SD': 'изображений Stable Diffusion',
            'MJ': 'генераций Midjourney',
            'DL3': 'изображений Dall-e 3',
        }
        for ai in ['GPT35', 'GPT4', 'VS', 'SD', 'MJ', 'DL3']:
            req = getattr(self, f'requests_{ai}')
            if req > 0:
                result.append(f'{req} {data[ai]}')
        return result + self.characteristics["details"]


class Subscription(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Пользователь')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name='Тариф')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписка'

    def __str__(self):
        return f'{self.user} | {self.tariff} | {self.end_date}'

    @property
    def is_expired(self):
        return datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.end_date


class Chat(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', verbose_name='Пользователь')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')
    is_current = models.BooleanField(default=False, verbose_name='Текущий чат')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return f'{self.user.username}: {self.pk}'

    def get_messages(self):
        return self.messages.select_related().filter(is_deleted=False).order_by('-pk')

    @property
    def get_name(self):
        messages = self.get_messages()
        text = messages.last().text if messages.exists() else 'Пустой чат'
        return f'{text[:20]}...' if len(text) > 20 else text

    def set_current(self):
        previous = Chat.objects.filter(user__pk=self.user.pk, is_current=True)
        if previous.exists():
            previous = previous.first()
            previous.is_current = False
            previous.save()
        self.is_current = True
        self.save()


class SampleCategory(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория шаблонов'
        verbose_name_plural = 'Категории шаблонов'

    def __str__(self):
        return self.name


class Sample(models.Model):

    name = models.CharField(max_length=50, null=True, verbose_name='Название')
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='Описание')
    categories = models.ManyToManyField(SampleCategory, verbose_name='Категории')
    text = models.TextField(verbose_name='Текст')
    variables = models.JSONField(default=dict, verbose_name='Переменные')
    use_context = models.BooleanField(default=True, verbose_name='Использовать контекст')

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def __str__(self):
        return self.name

    def get_variables(self):
        return re.findall(r'\[TEXT[0-9+]?]', str(self.text))

    @property
    def get_categories(self):
        return self.categories.all()


class UserSample(Sample):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='samples', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Пользовательский шаблон'
        verbose_name_plural = 'Пользовательские шаблоны'


class UserSamplesLikes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='likes', verbose_name='Шаблон')

    class Meta:
        verbose_name = 'Избранный шаблон'
        verbose_name_plural = 'Избранные шаблоны'

    def __str__(self):
        return f'{self.user.pk} - {self.sample.pk}'


class Message(models.Model):

    AI = (
        ('GPT35', 'GPT-3.5'),
        ('GPT4', 'GPT-4'),
        ('VS', 'Vision'),
        ('SD', 'Stable Diffusion'),
        ('MJ', 'Midjourney'),
        ('DL3', 'Dall-e 3')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='Пользователь')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, related_name='messages', verbose_name='Чат')
    is_sender = models.BooleanField(default=True, verbose_name='Отправитель')
    used_ai = models.CharField(choices=AI, null=True, blank=True, verbose_name='Использованная нейросеть')
    from_subscription = models.BooleanField(default=True, verbose_name='Запрос по подписке')
    sample = models.ForeignKey(Sample, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Шаблон')
    text = models.TextField(blank=True, verbose_name='Текст')
    time = models.DateTimeField(auto_now=True, verbose_name='Время отправки')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.user.username}: {self.text[:10]}...'

    @property
    def get_attachment(self):
        attachment = self.attachment.select_related()
        if not attachment.exists():
            return None
        url = attachment.first().file.url
        return [url, url.split('.')[-1]]


class Attachment(models.Model):

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachment', verbose_name='Сообщение')
    file = models.FileField(upload_to='attachments', verbose_name='Файл')

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

    def __str__(self):
        return self.file.name

    def __del__(self):
        pass


class NewChatCategory(models.Model):

    SECTIONS = (
        ('1', 'Текстовая нейросеть'),
        ('2', 'Создание картинок'),
        ('3', 'Для специалистов')
    )

    name = models.CharField(max_length=128, verbose_name='Название')
    section = models.CharField(choices=SECTIONS, default=SECTIONS[0][0], verbose_name='Раздел')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория для нового чата'
        verbose_name_plural = 'Категории для нового чата'

    def __str__(self):
        return self.name

    @property
    def get_samples(self):
        return self.samples.select_related().all()


class NewChatSample(models.Model):

    SECTIONS = (
        ('1', 'Текстовая нейросеть'),
        ('2', 'Создание картинок'),
        ('3', 'Для специалистов')
    )

    text = models.TextField(verbose_name='Текст запроса')
    icon = models.ImageField(upload_to='new_chat_icons', null=True, blank=True, verbose_name='Иконка')
    section = models.CharField(choices=SECTIONS, null=True, blank=True, verbose_name='Раздел')
    category = models.ForeignKey(NewChatCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='samples', verbose_name='Категория')
    for_free_version = models.JSONField(default=dict, verbose_name='Примеры изображений для бесплатной версии')

    class Meta:
        verbose_name = 'Шаблон для нового чата'
        verbose_name_plural = 'Шаблоны для нового чата'

    def __str__(self):
        return f'{self.text[:10]}...'

    @property
    def check_sd(self):
        return 'sd' in self.for_free_version.keys()

    @property
    def check_mj(self):
        return 'mj' in self.for_free_version.keys()

    @property
    def check_dl3(self):
        return 'dl3' in self.for_free_version.keys()


class NewChatInstruction(models.Model):

    name = models.CharField(max_length=36, verbose_name='Название')
    description = models.CharField(max_length=128, verbose_name='Описание')

    class Meta:
        verbose_name = 'Пункт туториала'
        verbose_name_plural = 'Пункты туториала'

    def __str__(self):
        return self.name


class PaymentOperation(models.Model):

    STATUSES = (
        ('I', 'Initiated'),
        ('S', 'Successful'),
        ('F', 'Failed')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations', verbose_name='Пользователь')
    status = models.CharField(choices=STATUSES, default=STATUSES[0][0], verbose_name='Статус')
    cost = models.FloatField(verbose_name='Сумма заказа')
    details = models.JSONField(default=dict, verbose_name='Детали')

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self):
        return f'{self.pk}-{self.user.username}-{self.details["subject"]}'


@receiver(models.signals.pre_save, sender=Subscription)
def set_start_date(sender, instance, raw, using, update_fields, *args, **kwargs):
    if not instance.pk:
        instance.start_date = datetime.now(pytz.timezone(settings.TIME_ZONE))


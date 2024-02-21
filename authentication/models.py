import math
from datetime import datetime, timedelta
import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from tochkagpt import settings


class User(AbstractUser):

    AI = (
        ('GPT-3.5', 'GPT-3.5'),
        ('GPT-4', 'GPT-4'),
    )

    IMG_AI = (
        ('Stable Diffusion', 'Stable Diffusion'),
        ('Midjourney', 'Midjourney'),
    )

    email_verified = models.BooleanField(default=True, verbose_name='Почта подтверждена')
    verification_key = models.CharField(max_length=128, blank=True, null=True, verbose_name='Ключ подтверждения почты')
    verification_key_expires = models.DateTimeField(blank=True, null=True, verbose_name='Ключ истекает')
    foreign_registration = models.BooleanField(default=True, verbose_name='Зарегистрирован через стороннее приложение')
    selected_ai = models.CharField(choices=AI, default=AI[0][0], max_length=256, verbose_name='Выбранная нейросеть')
    selected_img_ai = models.CharField(choices=IMG_AI, default=IMG_AI[0][0], max_length=256, verbose_name='Выбранная нейросеть для изображений')
    requests_GPT35 = models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (GPT-3.5)')
    requests_GPT4 = models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (GPT-4)')
    requests_VS = models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Vision)')
    requests_SD = models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Stable Diffusion)')
    requests_MJ = models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Midjourney)')
    requests_DL3 = models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Dall-e 3)')
    use_context = models.BooleanField(default=True, verbose_name='Использовать контекст')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_verification_key_expired(self):
        return datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.verification_key_expires + timedelta(hours=48)

    @property
    def get_subscription(self):
        query = self.subscriptions.select_related().filter(
            end_date__gte=datetime.now(pytz.timezone(settings.TIME_ZONE)))
        if query.exists():
            return query[0]
        else:
            return None

    def check_ai(self, ai):
        subscription = self.get_subscription
        if (subscription is not None and getattr(subscription.tariff, f'requests_{ai}') > 0) or ai == 'GPT35':
            return True
        return False

    @property
    def check_gpt35(self):
        return self.check_ai('GPT35')

    @property
    def check_gpt4(self):
        return self.check_ai('GPT4')

    @property
    def check_sd(self):
        return self.check_ai('SD')

    @property
    def check_mj(self):
        return self.check_ai('MJ')

    @property
    def has_img_ai(self):
        subscription = self.get_subscription
        return False if subscription is None or \
                        (subscription.tariff.requests_MJ == 0 and subscription.tariff.requests_SD == 0) else True

    @property
    def get_day_requests(self):
        start_time = datetime.now(pytz.timezone(settings.TIME_ZONE)).replace(hour=0, minute=0, second=0, microsecond=0)
        return len(self.messages.select_related().filter(is_sender=False, time__gte=start_time,
                                                         from_subscription=False))

    def get_month_requests(self, ai):
        now = datetime.now(pytz.timezone(settings.TIME_ZONE))
        sub_start_date = self.get_subscription.start_date
        months_count = math.floor((now - sub_start_date) / timedelta(days=30))
        start_date = sub_start_date + timedelta(days=30*months_count)

        return len(self.messages.select_related().filter(is_sender=False, time__gte=start_date, used_ai=ai,
                                                         from_subscription=True))

    @property
    def get_month_gpt35(self):
        return 0 if self.get_subscription is None else\
            max(self.get_subscription.tariff.requests_GPT35 - self.get_month_requests('GPT35'), 0)

    @property
    def get_month_gpt4(self):
        return 0 if self.get_subscription is None else\
            max(self.get_subscription.tariff.requests_GPT4 - self.get_month_requests('GPT4') - self.get_month_requests('GPT35'), 0)

    @property
    def get_month_vs(self):
        return 0 if self.get_subscription is None else\
            max(self.get_subscription.tariff.requests_VS - self.get_month_requests('VS'), 0)

    @property
    def get_month_sd(self):
        return 0 if self.get_subscription is None else\
            max(self.get_subscription.tariff.requests_VS - self.get_month_requests('SD'), 0)

    @property
    def get_month_mj(self):
        return 0 if self.get_subscription is None else\
            max(self.get_subscription.tariff.requests_VS - self.get_month_requests('MJ'), 0)

    @property
    def get_month_dl3(self):
        return 0 if self.get_subscription is None else\
            max(self.get_subscription.tariff.requests_VS - self.get_month_requests('DL3'), 0)

    @property
    def get_samples(self):
        return self.samples.select_related().all()

    @property
    def get_liked_samples(self):
        return [like.sample for like in self.likes.select_related().all()]

    @property
    def get_current_chat(self):
        current = self.chats.select_related().filter(is_current=True)
        return current.first() if current.exists() > 0 else None


@receiver(models.signals.pre_save, sender=User)
def set_username(sender, instance, raw, using, update_fields, *args, **kwargs):
    instance.username = instance.email

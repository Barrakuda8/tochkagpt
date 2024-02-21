from django.db import models


class Review(models.Model):

    user_name = models.CharField(max_length=32, verbose_name='Имя пользователя')
    user_tag = models.CharField(max_length=16, verbose_name='Тэг пользователя')
    user_photo = models.ImageField(upload_to='user_photos', verbose_name='Фото пользователя')
    text = models.TextField(verbose_name='Текст отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.user_name}: {self.text[:10]}...'

    @property
    def get_user_tag(self):
        return self.user_tag if self.user_tag.startswith('@') else f'@{self.user_tag}'


class FAQCategory(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория вопросов'
        verbose_name_plural = 'Категории вопросов'

    def __str__(self):
        return self.name


class FAQ(models.Model):

    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    home_page = models.BooleanField(default=False, verbose_name='Отображать на главной')
    business_page = models.BooleanField(default=False, verbose_name='Отображать на странице для бизнеса')
    categories = models.ManyToManyField(FAQCategory, blank=True, verbose_name='Категории')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.question[:20]}...'

    @property
    def get_category_classes(self):
        return ''.join([f' category-{c.pk}' for c in self.categories.all()])


class ArticleCategory(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория статей'
        verbose_name_plural = 'Категории статей'

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.TextField(verbose_name='Заголовок')
    second_title = models.TextField(null=True, blank=True, verbose_name='Подзаголовок')
    photo = models.ImageField(upload_to='article_photos', blank=True, verbose_name='Заглавное фото')
    categories = models.ManyToManyField(ArticleCategory, blank=True, verbose_name='Категории')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.title[:20]}...'

    @property
    def get_category_classes(self):
        return ''.join([f' category-{c.pk}' for c in self.categories.all()])


class Client(models.Model):

    image = models.ImageField(upload_to='clients', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.image.url

from django.urls import path
import main.views as main

app_name = 'main'

urlpatterns = [
    path('', main.index, name='index'),
    path('business/', main.business, name='business'),
    path('rules', main.rules, name='rules'),
    path('blog/', main.blog, name='blog'),
    path('article/<int:pk>', main.article, name='article'),
    path('faq/', main.faq, name='faq'),
]
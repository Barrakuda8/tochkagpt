from django.shortcuts import render
from chat.models import Tariff
from main.models import FAQ, Review, FAQCategory, Article, ArticleCategory


def index(request):

    context = {
        'title': 'точкаGPT | ChatGPT на русском',
        'faqs': FAQ.objects.filter(home_page=True),
        'reviews': Review.objects.all().order_by('-pk')[:6],
        'tariffs': Tariff.objects.all().order_by('price'),
    }

    return render(request, 'main/index.html', context=context)


def business(request):

    context = {
        'title': 'точкаGPT для компаний',
        'faqs': FAQ.objects.filter(business_page=True)
    }

    return render(request, 'main/business.html', context=context)


def rules(request):

    context = {
        'title': 'Публичный договор',
    }

    return render(request, 'main/rules.html', context=context)


def blog(request):

    context = {
        'title': 'Блог',
        'articles': Article.objects.all(),
        'categories': ArticleCategory.objects.all()
    }

    return render(request, 'main/blog.html', context=context)


def article(request, pk):

    context = {
        'article': Article.objects.get(pk=pk)
    }

    return render(request, 'main/article.html', context=context)


def faq(request):

    context = {
        'title': 'Часто задаваемые вопросы',
        'faqs': FAQ.objects.all(),
        'categories': FAQCategory.objects.all()
    }

    return render(request, 'main/faq.html', context=context)

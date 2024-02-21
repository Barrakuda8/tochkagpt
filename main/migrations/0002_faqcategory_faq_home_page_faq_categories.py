# Generated by Django 5.0.1 on 2024-01-24 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория статей',
                'verbose_name_plural': 'Категории статей',
            },
        ),
        migrations.AddField(
            model_name='faq',
            name='home_page',
            field=models.BooleanField(default=False, verbose_name='Отображать на главной'),
        ),
        migrations.AddField(
            model_name='faq',
            name='categories',
            field=models.ManyToManyField(to='main.faqcategory', verbose_name='Категории'),
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-13 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_sample_use_context_alter_tariff_samples_included'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewChatCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('icon', models.ImageField(upload_to='new_chat_icons', verbose_name='Иконка')),
                ('section', models.CharField(choices=[('1', 'Текстовая нейросеть'), ('2', 'Создание картинок'), ('3', 'Для специалистов')], default='1', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Категория для нового чата',
                'verbose_name_plural': 'Категории для нового чата',
            },
        ),
        migrations.CreateModel(
            name='NewChatSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст запроса')),
                ('icon', models.ImageField(upload_to='new_chat_icons', verbose_name='Иконка')),
                ('section', models.CharField(blank=True, choices=[('1', 'Текстовая нейросеть'), ('2', 'Создание картинок'), ('3', 'Для специалистов')], null=True, verbose_name='Раздел')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.newchatcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Шаблон для нового чата',
                'verbose_name_plural': 'Шаблоны для нового чата',
            },
        ),
    ]

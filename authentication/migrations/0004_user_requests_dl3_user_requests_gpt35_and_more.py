# Generated by Django 5.0.1 on 2024-02-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_selected_ai_user_selected_img_ai'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='requests_DL3',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Dall-e 3)'),
        ),
        migrations.AddField(
            model_name='user',
            name='requests_GPT35',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (GPT-3.5)'),
        ),
        migrations.AddField(
            model_name='user',
            name='requests_GPT4',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (GPT-4)'),
        ),
        migrations.AddField(
            model_name='user',
            name='requests_MJ',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Midjourney)'),
        ),
        migrations.AddField(
            model_name='user',
            name='requests_SD',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Stable Diffusion)'),
        ),
        migrations.AddField(
            model_name='user',
            name='requests_VS',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество дополнительных запросов (Vision)'),
        ),
    ]

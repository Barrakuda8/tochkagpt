# Generated by Django 5.0.1 on 2024-04-22 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0028_alter_subscription_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='bottom_description',
            field=models.TextField(null=True, verbose_name='Нижнее описание'),
        ),
        migrations.AddField(
            model_name='tariff',
            name='top_description',
            field=models.TextField(null=True, verbose_name='Верхнее описание'),
        ),
    ]

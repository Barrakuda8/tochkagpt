# Generated by Django 5.0.1 on 2024-02-13 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_remove_newchatcategory_icon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newchatcategory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
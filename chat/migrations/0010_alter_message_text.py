# Generated by Django 5.0.1 on 2024-02-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_chat_is_current_alter_attachment_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(blank=True, verbose_name='Текст'),
        ),
    ]

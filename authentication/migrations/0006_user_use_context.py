# Generated by Django 5.0.1 on 2024-02-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_selected_ai_alter_user_selected_img_ai'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='use_context',
            field=models.BooleanField(default=True, verbose_name='Использовать контекст'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0027_alter_paymentoperation_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='start_date',
            field=models.DateTimeField(verbose_name='Дата начала'),
        ),
    ]

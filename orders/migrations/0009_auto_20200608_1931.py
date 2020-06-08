# Generated by Django 3.0.7 on 2020-06-08 19:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]

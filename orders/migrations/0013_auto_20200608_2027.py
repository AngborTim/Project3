# Generated by Django 3.0.7 on 2020-06-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20200608_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmporder',
            name='order_id',
            field=models.CharField(default='54192', max_length=64),
        ),
    ]
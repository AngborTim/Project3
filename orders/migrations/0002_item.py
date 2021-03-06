# Generated by Django 3.0.7 on 2020-06-05 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('has_extra_toppings', models.IntegerField(default=0)),
                ('priceSmall', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('priceLarge', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('itemtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemtype', to='orders.ItemType')),
            ],
        ),
    ]

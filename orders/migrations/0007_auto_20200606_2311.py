# Generated by Django 3.0.5 on 2020-06-06 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200606_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
    ]

# Generated by Django 3.0.5 on 2020-06-04 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200604_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='create_date',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
# Generated by Django 3.0.8 on 2020-11-16 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20201117_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

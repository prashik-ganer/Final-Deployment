# Generated by Django 3.0.8 on 2021-01-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0054_auto_20210116_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.CharField(max_length=2000),
        ),
    ]

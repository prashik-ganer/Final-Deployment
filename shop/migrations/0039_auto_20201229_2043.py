# Generated by Django 3.0.8 on 2020-12-29 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_auto_20201226_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=500),
        ),
    ]

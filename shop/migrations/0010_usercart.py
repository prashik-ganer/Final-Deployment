# Generated by Django 3.0.8 on 2020-10-29 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20201024_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('usercart', models.CharField(max_length=5000)),
            ],
        ),
    ]

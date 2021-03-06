# Generated by Django 3.0.8 on 2020-12-09 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_customer_qr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='mode',
            field=models.CharField(blank=True, choices=[('Pickup', 'Pickup'), ('Delivery', 'Delivery')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=200, null=True),
        ),
    ]

# Generated by Django 3.1 on 2024-12-13 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

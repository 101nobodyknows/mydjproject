# Generated by Django 5.0.6 on 2024-07-01 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_new_product_product_availability_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new_product',
            name='product_review',
        ),
        migrations.AddField(
            model_name='new_product',
            name='product_rating',
            field=models.IntegerField(default=5),
        ),
    ]

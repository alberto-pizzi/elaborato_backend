# Generated by Django 5.0.6 on 2024-06-20 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='image_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.image'),
        ),
    ]
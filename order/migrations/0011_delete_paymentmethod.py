# Generated by Django 5.0.6 on 2024-06-10 16:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0010_paymentmethod_alter_order_address_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PaymentMethod",
        ),
    ]

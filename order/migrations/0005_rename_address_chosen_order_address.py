# Generated by Django 5.0.6 on 2024-06-09 13:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0004_remove_order_total_order_address_chosen_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="address_chosen",
            new_name="address",
        ),
    ]

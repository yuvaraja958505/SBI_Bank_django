# Generated by Django 5.0.2 on 2024-09-28 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0002_customer_register_table_account_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer_register_table',
            old_name='registered_datetime',
            new_name='registered_dt',
        ),
    ]

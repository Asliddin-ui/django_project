# Generated by Django 4.1.1 on 2022-09-27 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0004_user_table_user_birthda_da6116_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='user',
            name='table_user_birthda_da6116_idx',
        ),
    ]

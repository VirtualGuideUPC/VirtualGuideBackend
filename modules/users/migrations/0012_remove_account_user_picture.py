# Generated by Django 3.2.3 on 2021-10-19 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_account_user_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='user_picture',
        ),
    ]

# Generated by Django 3.2.3 on 2021-07-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210702_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferencecategory',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='preferencetypeplace',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]

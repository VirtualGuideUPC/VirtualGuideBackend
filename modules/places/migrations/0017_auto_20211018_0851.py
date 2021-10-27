# Generated by Django 3.2.3 on 2021-10-18 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0016_alter_touristicplacecategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touristicplacecategory',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='places.category'),
        ),
        migrations.AlterField(
            model_name='touristicplacecategory',
            name='touristic_place',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='places.touristicplace'),
        ),
    ]
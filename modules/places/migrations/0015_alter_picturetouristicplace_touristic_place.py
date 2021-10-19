# Generated by Django 3.2.3 on 2021-10-18 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0014_alter_picturetouristicplace_touristic_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picturetouristicplace',
            name='touristic_place',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='places.touristicplace'),
        ),
    ]
# Generated by Django 4.0.6 on 2022-07-16 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_city_id_car_city_rename_engine_id_car_engine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.set'),
        ),
    ]

# Generated by Django 4.1 on 2022-10-14 11:41

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0027_files_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminEntryFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DistributorEntryFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=core.models.CSVFileStorage(), upload_to='distributor/csv/', verbose_name='CSV файл')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'CSV файл',
                'verbose_name_plural': 'CSV файлы',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SetEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.distributor', verbose_name='Дистрибьютор')),
            ],
            options={
                'verbose_name': 'Заявка дистрибьютора',
                'verbose_name_plural': 'Заявки дистрибьюторов',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время создания'),
        ),
        migrations.DeleteModel(
            name='Files',
        ),
        migrations.AddField(
            model_name='setentry',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.entry', verbose_name='Заявка'),
        ),
    ]
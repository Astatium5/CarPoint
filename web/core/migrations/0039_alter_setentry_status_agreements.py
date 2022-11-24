# Generated by Django 4.1 on 2022-11-24 18:56

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0038_remove_setentry_is_shipped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setentry',
            name='status',
            field=models.CharField(choices=[('new', 'Ожидает'), ('shipped', 'Отгружен'), ('road', 'В пути'), ('client', 'Передан клиенту'), ('payment', 'Ожидает оплаты'), ('complete', 'Закрыто')], default='new', max_length=32, verbose_name='Статус заявки'),
        ),
        migrations.CreateModel(
            name='Agreements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement', models.FileField(blank=True, default=None, storage=core.models.DealerFileStorage(), upload_to='files/agreements', verbose_name='Соглашение')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Дилер')),
            ],
        ),
    ]

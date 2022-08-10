# Generated by Django 4.0.6 on 2022-08-10 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_city_options_alter_mark_options_entry'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('image', models.URLField(verbose_name='Картинка')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Новинка',
                'verbose_name_plural': 'Новинки',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.AlterField(
            model_name='entry',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.car', verbose_name='Автомобиль'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='email',
            field=models.CharField(max_length=255, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='phone',
            field=models.BigIntegerField(verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.botuser', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='username',
            field=models.CharField(max_length=255, null=True, verbose_name='Имя пользователя'),
        ),
    ]
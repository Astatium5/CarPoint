# Generated by Django 4.0.6 on 2022-08-08 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_color_setcolor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['title'], 'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AlterModelOptions(
            name='mark',
            options={'ordering': ['title'], 'verbose_name': 'Марка', 'verbose_name_plural': 'Марки'},
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.BigIntegerField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.botuser')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]

# Generated by Django 4.1 on 2022-10-15 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_adminentryfiles_entry_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminentryfiles',
            name='entry',
        ),
        migrations.RemoveField(
            model_name='distributorentryfiles',
            name='entry',
        ),
    ]
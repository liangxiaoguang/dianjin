# Generated by Django 2.0 on 2019-01-07 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0004_auto_20190107_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duowan',
            name='home_url',
        ),
        migrations.RemoveField(
            model_name='hupu',
            name='home_url',
        ),
        migrations.RemoveField(
            model_name='xinlang',
            name='home_url',
        ),
    ]

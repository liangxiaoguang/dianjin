# Generated by Django 2.0 on 2019-01-01 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0002_auto_20190101_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duowan',
            name='style',
            field=models.CharField(default='其他', max_length=50),
        ),
        migrations.AlterField(
            model_name='hupu',
            name='style',
            field=models.CharField(default='其他', max_length=50),
        ),
    ]
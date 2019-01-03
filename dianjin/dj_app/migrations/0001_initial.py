# Generated by Django 2.0 on 2018-12-31 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='duowan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.CharField(max_length=50, unique=True)),
                ('c_time', models.CharField(max_length=50)),
                ('c_title', models.CharField(max_length=500)),
                ('now_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('pic', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='hupu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.CharField(max_length=50, unique=True)),
                ('c_time', models.CharField(max_length=50)),
                ('c_title', models.CharField(max_length=500)),
                ('now_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('pic', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='xinlang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.CharField(max_length=50, unique=True)),
                ('c_time', models.CharField(max_length=50)),
                ('c_title', models.CharField(max_length=500)),
                ('now_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('pic', models.CharField(max_length=500)),
            ],
        ),
    ]

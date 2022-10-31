# Generated by Django 4.1.2 on 2022-10-31 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('USER_ID', models.CharField(max_length=20)),
                ('USER_NAME', models.CharField(max_length=40)),
                ('USER_BIRTH', models.CharField(max_length=8)),
                ('USER_PHONE', models.CharField(max_length=15)),
                ('USER_EMAIL', models.EmailField(max_length=254)),
                ('CRTIME', models.DateTimeField(auto_now_add=True)),
                ('DISCARD', models.BooleanField(default=False)),
            ],
        ),
    ]

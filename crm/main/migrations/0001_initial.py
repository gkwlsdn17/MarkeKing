# Generated by Django 4.1.2 on 2022-10-31 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CUSTOMER_ID', models.CharField(max_length=20)),
                ('CUSTOMER_PW', models.CharField(max_length=40)),
                ('CUSTOMER_NAME', models.CharField(max_length=40)),
                ('CUSTOMER_BIRTH', models.CharField(max_length=8)),
                ('CUSTOMER_PHONE', models.CharField(max_length=15)),
                ('CUSTOMER_EMAIL', models.EmailField(max_length=254)),
                ('CUSTOMER_ADDR', models.CharField(max_length=300)),
                ('FIRST_VISIT', models.DateTimeField(auto_now_add=True)),
                ('LAST_VISIT', models.DateTimeField()),
                ('CUSTOMER_RATING', models.IntegerField(default=0)),
                ('CRTIME', models.DateTimeField(auto_now=True)),
                ('DISCARD', models.BooleanField(default=False)),
            ],
        ),
    ]
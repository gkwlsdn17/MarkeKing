# Generated by Django 4.1 on 2022-12-08 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_customer_customer_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='CUSTOMER_SEX',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='CUSTOMER_ZIPCODE',
            field=models.CharField(default='', max_length=10),
        ),
    ]

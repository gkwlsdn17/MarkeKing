# Generated by Django 4.1.2 on 2022-11-30 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='CUSTOMER_RATING',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='main.rating'),
        ),
    ]
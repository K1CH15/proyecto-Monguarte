# Generated by Django 4.2.2 on 2023-10-09 23:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio_unitario',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]

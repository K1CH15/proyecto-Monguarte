# Generated by Django 4.2.2 on 2023-08-19 21:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('nombre', models.CharField(max_length=45, verbose_name='Nombre')),
                ('precio_unitario', models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('stock', models.PositiveIntegerField(default=0, editable=False, verbose_name='Stock de Materia Prima')),
                ('estado', models.CharField(choices=[('1', 'Activo'), ('0', 'Inactivo')], default='1', max_length=1, verbose_name='Estado')),
                ('tamano', models.CharField(choices=[('1', 'Pequeño'), ('2', 'Mediano'), ('3', 'Grande')], max_length=1, verbose_name='Tamaño')),
                ('tipo', models.CharField(choices=[('1', 'Prenda de vestir'), ('2', 'Accesorio'), ('3', 'Figura')], max_length=1, verbose_name='Tipo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

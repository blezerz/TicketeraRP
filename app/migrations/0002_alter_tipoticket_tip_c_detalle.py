# Generated by Django 5.1.1 on 2024-11-21 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoticket',
            name='tip_c_detalle',
            field=models.CharField(max_length=100),
        ),
    ]
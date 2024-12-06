# Generated by Django 4.2.5 on 2024-12-05 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_ticket_archivos_adjuntos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='archivo_adjunto',
        ),
        migrations.CreateModel(
            name='ArchivoAdjunto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='archivos_adjuntos/')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archivos_adjuntos', to='app.ticket')),
            ],
        ),
    ]
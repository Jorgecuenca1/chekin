# Generated by Django 4.0.5 on 2022-07-23 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_profile_razon_social'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventos',
            name='aprobado',
            field=models.CharField(blank=True, choices=[('SI', 'SI'), ('NO', 'NO')], max_length=10, null=True, verbose_name='Aprobado?'),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_profile_historialcar_alter_acomodacion_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='boleta',
            name='code',
            field=models.ImageField(blank=True, null=True, upload_to='boleta/code', verbose_name='Imagen de la firma del usuario'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='historialcar',
            field=models.ManyToManyField(blank=True, null=True, related_name='Historial', to='users.carshop'),
        ),
    ]

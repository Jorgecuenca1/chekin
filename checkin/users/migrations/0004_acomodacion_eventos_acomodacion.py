# Generated by Django 4.0.5 on 2022-06-17 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_etapa_fechafinal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acomodacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, verbose_name='Nombre de acomodación')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Acomodación',
                'verbose_name_plural': 'Acomodaciones',
            },
        ),
        migrations.AddField(
            model_name='eventos',
            name='acomodacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.acomodacion', verbose_name='Acomodación'),
        ),
    ]

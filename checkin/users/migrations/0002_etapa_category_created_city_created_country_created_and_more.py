# Generated by Django 4.0.5 on 2022-06-17 16:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Nombre ')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('capacity', models.CharField(max_length=254, verbose_name='Capacidad ')),
                ('price', models.CharField(max_length=254, verbose_name='Precio ')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Etapa',
                'verbose_name_plural': 'Etapas',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventos',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventos',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='usuario/firma', verbose_name='Imagen de la firma del usuario'),
        ),
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='region',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typedocument',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Nombre ')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('capacity', models.CharField(max_length=254, verbose_name='Capacidad ')),
                ('price', models.CharField(max_length=254, verbose_name='Precio ')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('etapa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.etapa', verbose_name='Etapa')),
            ],
            options={
                'verbose_name': 'Localidad',
                'verbose_name_plural': 'Localidades',
            },
        ),
        migrations.AddField(
            model_name='eventos',
            name='etapa',
            field=models.ManyToManyField(blank=True, null=True, to='users.etapa', verbose_name='Etapa'),
        ),
        migrations.AddField(
            model_name='eventos',
            name='localidad',
            field=models.ManyToManyField(blank=True, null=True, to='users.localidad', verbose_name='Localidad'),
        ),
    ]

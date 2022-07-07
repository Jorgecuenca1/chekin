# Generated by Django 4.0.5 on 2022-07-05 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_eventos_participante_eventos_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank='True', max_length=200, null='True', verbose_name='Título')),
                ('image', models.ImageField(blank=True, null=True, upload_to='usuario/firma', verbose_name='Imagen de la firma del usuario')),
                ('descripcion', models.TextField(blank='True', null='True', verbose_name='Título')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.category', verbose_name='Categoría')),
                ('evento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.eventos', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
            },
        ),
    ]

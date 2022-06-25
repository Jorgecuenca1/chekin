# Generated by Django 3.1.1 on 2022-06-25 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20220623_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sucess', models.CharField(blank=True, max_length=10, null=True, verbose_name='satisfactorio')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Revisar',
                'verbose_name_plural': 'Revisados',
            },
        ),
    ]
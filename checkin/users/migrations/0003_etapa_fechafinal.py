# Generated by Django 4.0.5 on 2022-06-17 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_etapa_category_created_city_created_country_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='fechafinal',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(verbose_name='Nombre del país', max_length=254)

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(verbose_name='Nombre del departamento', max_length=254)
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return '{} | {}'.format(self.country.name, self.name)


class City(models.Model):
    name = models.CharField(verbose_name='Nombre municipio', max_length=254)
    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

    def __str__(self):
        return '{} | {} | {}'.format(self.state.country.name, self.state.name, self.name)

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)
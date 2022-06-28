from django.db import models
from django.contrib.auth.models import User
SEX_CHOICES = (
        ('F', 'Femenino',),
        ('M', 'Masculino',),
        ('O', 'Otro',),
    )
CHOICES = (
        ('SI', 'SI',),
        ('NO', 'NO',),
    )
ESTADO_CHOICES = (
        ('PAGO', 'PAGO',),
        ('NOPAGO', 'NOPAGO',),

    )
# Create your models here.
class Country(models.Model):
    name = models.CharField(verbose_name='Nombre del país', max_length=254)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'

    def __str__(self):
        return self.name


class Etapa(models.Model):
    name = models.CharField(verbose_name= 'Nombre ', max_length=254)
    fecha = models.DateTimeField(auto_now=False, blank=True, null=True)
    fechafinal = models.DateTimeField(auto_now=False, blank=True, null=True)
    capacity = models.CharField(verbose_name='Capacidad ', max_length=254)
    price = models.CharField(verbose_name='Precio ', max_length=254)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'

    def __str__(self):
        return self.name
class Localidad(models.Model):
    name = models.CharField(verbose_name='Nombre ', max_length=254)
    fecha = models.DateTimeField(auto_now=False, blank=True, null=True)
    capacity = models.CharField(verbose_name='Capacidad ', max_length=254)
    etapa = models.ForeignKey(Etapa, verbose_name='Etapa',
                                      on_delete=models.PROTECT,
                                      blank=True, null=True)
    price = models.CharField(verbose_name='Precio ', max_length=254)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(verbose_name='Nombre del departamento', max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return '{} | {}'.format(self.country.name, self.name)


class City(models.Model):
    name = models.CharField(verbose_name='Nombre municipio', max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

    def __str__(self):
        return '{} | {} | {}'.format(self.state.country.name, self.state.name, self.name)

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)
class TypeDocument(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name='Tipo de documento')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'TIpo de documentos'


class Acomodacion(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name='Nombre de acomodación')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Acomodación'
        verbose_name_plural = 'Acomodaciones'
class Puntosventa(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name='Nombre de categoria')
    image = models.ImageField(verbose_name='Foto de local', upload_to='puntoventa', blank=True,
                              null=True)
    adress = models.CharField(verbose_name='Dirección', max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    horario = models.TextField(verbose_name='Horario', blank=True, null=True)
    facebook = models.CharField(verbose_name='Facebook', max_length=300, blank=True, null=True)
    instagram = models.CharField(verbose_name='Instagram', max_length=300, blank=True, null=True)
    twitter = models.CharField(verbose_name='Twitter', max_length=300, blank=True, null=True)
    tiktok = models.CharField(verbose_name='TIktok', max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Category(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name='Nombre de categoria')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
class Convencion(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name='Nombre de convenciones')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Convencion'
        verbose_name_plural = 'Convenciones'
class Boleta(models.Model):
    localidad = models.ForeignKey(Localidad, verbose_name='Localidad',
                                      on_delete=models.PROTECT,
                                      blank=True, null=True)
    capacity = models.CharField(verbose_name='Cantidad idsponible', max_length=254)
    asientos = models.CharField(verbose_name='Asientos', max_length=254)
    price = models.CharField(verbose_name='Precio ', max_length=254)
    leyenda = models.CharField(verbose_name='Leyenda', max_length=254)
    convencion = models.ForeignKey(Convencion, verbose_name='Localidad',
                                  on_delete=models.PROTECT,
                                  blank=True, null=True)
    comprada = models.CharField(max_length=10, choices=CHOICES, verbose_name='Comprada', null=True,
                                            blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'BOleta'
        verbose_name_plural = 'Boleta'

    def __str__(self):
        return self.capacity
class CarShop(models.Model):
    boleta = models.ManyToManyField(Boleta, verbose_name='Boletas',
                                    blank=True, null=True)
    comprada = models.CharField(max_length=10, choices=ESTADO_CHOICES, verbose_name='Comprada', null=True,
                                blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.comprada) or ''

    class Meta:
        verbose_name = 'Carro de compra'
        verbose_name_plural = 'Carros de compra'
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    car = models.OneToOneField(CarShop,on_delete=models.PROTECT, blank=True, null=True)
    historialcar = models.ManyToManyField(CarShop, related_name='Historial', blank=True, null=True)
    email = models.EmailField(max_length=200, verbose_name='Correo electronico', blank=True, null=True)
    first_name = models.CharField(max_length=200, verbose_name='Nombres', blank=True)
    last_name = models.CharField(max_length=200, verbose_name='Apellidos', blank=True)
    type_document = models.ForeignKey(TypeDocument, verbose_name='1.7. TIPO DOCUMENTO IDENTIDAD',
                                      on_delete=models.PROTECT,
                                      blank=True, null=True)
    identification = models.IntegerField( verbose_name='Número de documento', blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, verbose_name='Sexo', null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now=False, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.ForeignKey(Country, verbose_name='País', on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(Region, verbose_name='Departamento', on_delete=models.PROTECT, blank=True, null=True)
    city = models.ForeignKey(City, verbose_name='Municipio', on_delete=models.PROTECT, blank=True, null=True)
    adress = models.CharField(verbose_name='Dirección',max_length=100,blank=True, null=True)
    type_house = models.CharField(verbose_name='Apartamento, unidad,edificio..', max_length=100, blank=True, null=True)
    neighbord = models.CharField(verbose_name='Barrio', max_length=100, blank=True,
                                  null=True)
    boleta = models.ManyToManyField(Boleta, verbose_name='Boletas',
                                         blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

class Eventos(models.Model):
    title = models.CharField(verbose_name='Título', blank='True', null='True', max_length=200)
    image = models.ImageField(verbose_name='Imagen de la firma del usuario', upload_to='usuario/firma', blank=True,
                              null=True)
    category = models.ForeignKey(Category, verbose_name='Categoría',
                                      on_delete=models.PROTECT,
                                      blank=True, null=True)
    acomodacion = models.ForeignKey(Acomodacion, verbose_name='Acomodación',
                                 on_delete=models.PROTECT,
                                 blank=True, null=True)
    minimum_age = models.IntegerField(verbose_name='Edad minima', blank=True, null=True)
    capacity = models.IntegerField( verbose_name='Aforo', blank=True, null=True)
    cantidadgeneral = models.IntegerField(verbose_name='Cantidad de boletas general', blank=True, null=True)
    cantidadvendidas = models.IntegerField(verbose_name='Cantidad de boletas general vendidas', blank=True, null=True)
    ventacomida = models.CharField(max_length=10, choices=CHOICES, verbose_name='Venta de comida', null=True, blank=True)
    ventalicor = models.CharField(max_length=10, choices=CHOICES, verbose_name='Venta de Licor', null=True,
                                   blank=True)
    lugar = models.CharField(max_length=10, verbose_name='Lugar', null=True,
                                  blank=True)
    inicio = models.CharField(max_length=10, verbose_name='Horario de inicio', null=True,
                             blank=True)
    final = models.CharField(max_length=10, verbose_name='Horario final', null=True,
                             blank=True)
    apertura = models.CharField(max_length=10, verbose_name='Apertura', null=True,
                             blank=True)
    accesodiscapacitados = models.CharField(max_length=10, choices=CHOICES, verbose_name='Acceso a personas con discapacidad', null=True,
                                   blank=True)
    accesoembarazadas = models.CharField(max_length=10, choices=CHOICES, verbose_name='Acceso a embarazadas', null=True,
                                            blank=True)
    descripcion = models.TextField(verbose_name='Descripción', blank='True', null='True')
    localidad = models.ManyToManyField(Localidad, verbose_name='Localidad',
                                      blank=True, null=True)
    puntosventa = models.ManyToManyField(Puntosventa, verbose_name='Punto de venta',
                                       blank=True, null=True)
    boleta = models.ManyToManyField(Boleta, verbose_name='Boletas',
                                    blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural= 'Eventos'

class Check(models.Model):
    sucess = models.CharField(max_length=10, verbose_name='satisfactorio', null=True,
                             blank=True)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return str(self.sucess) or ''

    class Meta:
        verbose_name = 'Revisar'
        verbose_name_plural= 'Revisados'
from django.contrib import admin
from .models import Country, Region, City, Profile, Eventos, Etapa, Localidad, Category, Puntosventa, Boleta, CarShop, \
    Check
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name',)
        }),
    )
    suit_form_tabs = (
        ('general', 'Nuevo país'),
    )


@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_filter = ('name', )
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name',)
        }),
    )
    suit_form_tabs = (
        ('general', 'Nuevo departamento'),
    )


@admin.register(City)
class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name', )
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name',)
        }),
    )
    suit_form_tabs = (
        ('general', 'Nuevo municipio'),
    )
@admin.register(Check)
class CheckAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'sucess',)
    list_filter = ('sucess', )
    search_fields = ('sucess',)

    suit_form_tabs = (
        ('general', 'Nueva sucess'),
    )
@admin.register(CarShop)
class CarShopAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'comprada',)
    list_filter = ('comprada', )
    search_fields = ('comprada',)

    suit_form_tabs = (
        ('general', 'Nueva Carro'),
    )
@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'first_name',)
    list_filter = ('first_name', )
    search_fields = ('first_name',)

    suit_form_tabs = (
        ('general', 'Nueva persona'),
    )

@admin.register(Eventos)
class EventosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('title', )
    search_fields = ('title',)

    suit_form_tabs = (
        ('general', 'Nueva Evwnto'),
    )

@admin.register(Etapa)
class EtapaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name', )
    search_fields = ('name',)

    suit_form_tabs = (
        ('general', 'Nueva Etapa'),
    )
@admin.register(Puntosventa)
class PuntosventaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name', )
    search_fields = ('name',)

    suit_form_tabs = (
        ('general', 'Nuevo punto de venta'),
    )
@admin.register(Boleta)
class PBoletaaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'capacity',)
    list_filter = ('capacity', )
    search_fields = ('capacity',)

    suit_form_tabs = (
        ('general', 'Nueva Boleta'),
    )
@admin.register(Localidad)
class LocalidadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name', )
    search_fields = ('name',)

    suit_form_tabs = (
        ('general', 'Nueva Localidad'),
    )

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name', )
    search_fields = ('name',)

    suit_form_tabs = (
        ('general', 'Nueva Localidad'),
    )
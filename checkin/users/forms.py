from django import forms
from django.forms import ModelForm, ClearableFileInput, SelectDateWidget, CheckboxSelectMultiple
from django.forms.fields import DateField
from .models import Eventos, Category, Acomodacion, Country, CHOICES, Region, City, Puntosventa, Artista, Sponsor


class EventosForm(forms.ModelForm):

    title = forms.CharField(label='Título', widget=forms.TextInput(attrs={"placeholder": "Título X",
                                                                          "class": "new-class-name two",
                                                                          "id": "my-id-for-textarea",
                                                                          "rows": 1,
                                                                          'cols': 80,
                                                                          'color': "blue",
                                                                          }))
    minimum_age = forms.CharField(label='Edad mínima', widget=forms.TextInput(attrs={"placeholder": "18",
                                                                                     "class": "new-class-name two",
                                                                                     "id": "my-id-for-textarea",
                                                                                     "rows": 1,
                                                                                     'cols': 80,
                                                                                     'color': "blue",
                                                                                     }))
    category = forms.ModelChoiceField(
        label='Categoría', queryset=Category.objects.all(),
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    acomodacion = forms.ModelChoiceField(
        label='Acomodación', queryset=Acomodacion.objects.all(),
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    ventacomida = forms.ChoiceField(
        label='Venta de comida', choices=CHOICES,
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    ventalicor = forms.ChoiceField(
        label='Venta de licor', choices=CHOICES,
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    accesoembarazadas = forms.ChoiceField(
        label='Acceso a embarazadas', choices=CHOICES,
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    accesodiscapacitados = forms.ChoiceField(
        label='Acceso a discapacitados', choices=CHOICES,
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    country = forms.ModelChoiceField(
        label='País', queryset=Country.objects.all(),
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    state = forms.ModelChoiceField(
        label='Departamento', queryset=Region.objects.all(),
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )
    city = forms.ModelChoiceField(
        label='Ciudad', queryset=City.objects.all(),
        widget=forms.Select(attrs={'style': 'color:#dbe2fb; background-color: #000'})
    )


    class Meta:
        model = Eventos
        exclude = ('created', 'aprobado','puntosventa','sponsor','participante')

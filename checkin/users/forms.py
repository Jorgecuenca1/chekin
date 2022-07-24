from django import forms
from django.forms import ModelForm, ClearableFileInput, SelectDateWidget, CheckboxSelectMultiple
from django.forms.fields import DateField
from .models import Eventos

class EventosForm(forms.ModelForm):
    title = forms.CharField(label='Título',
                                widget=forms.TextInput(attrs={"placeholder": "Título",
                                                             "class": "new-class-name two",
                                                             "id": "my-id-for-textarea",
                                                             "rows": 1,
                                                             'cols': 80,
                                                              'color': "blue",
                                                             }))
    class Meta:
        model = Eventos
        exclude = ('created','aprobado')
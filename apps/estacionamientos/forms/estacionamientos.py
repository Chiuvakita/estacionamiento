from django import forms
from ..models.estacionamiento import Estacionamiento

class EstacionamientoForm(forms.ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ["estado", "tipo"]

class EstacionamientosMasivoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1)
    tipo = forms.ChoiceField(choices=Estacionamiento.TIPO_CHOICES)

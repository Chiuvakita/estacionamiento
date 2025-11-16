from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ["patente", "marca", "modelo", "tipo"]
        widgets = {
            "patente": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.TextInput(attrs={"class": "form-control"}),
        }

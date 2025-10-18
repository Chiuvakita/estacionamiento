from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente', 'marca', 'modelo', 'tipo']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patente'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo'}),
        }

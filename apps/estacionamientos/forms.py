from django import forms
from django.utils import timezone
from .models import Estacionamiento, Reserva

class EstacionamientoForm(forms.ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ["estado", "tipo"]

class EstacionamientosMasivoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1)
    tipo = forms.ChoiceField(choices=Estacionamiento.TIPO_CHOICES)

class ReservaCrearForm(forms.Form):
    patente = forms.CharField(max_length=10)
    estacionamiento_id = forms.IntegerField()
    fecha_inicio = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])
    duracion = forms.IntegerField(min_value=1)

    def clean(self):
        data = super().clean()
        if "fecha_inicio" in data:
            if data["fecha_inicio"].date() == timezone.now().date():
                raise forms.ValidationError("No puedes reservar para el mismo día.")
            if data["fecha_inicio"] < timezone.now():
                raise forms.ValidationError("La fecha no puede ser pasada.")
        return data


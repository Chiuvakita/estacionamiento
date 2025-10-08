from django import forms
from django.utils import timezone
from ..models.reserva import Reserva  

class ReservaCrearForm(forms.Form):
    patente = forms.CharField(max_length=10)
    estacionamiento_id = forms.IntegerField()
    fecha_inicio = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])
    duracion = forms.IntegerField(min_value=1)

    def clean(self):
        data = super().clean()
        if "fecha_inicio" in data and data["fecha_inicio"] is not None:
            now = timezone.now()
            if data["fecha_inicio"].date() == now.date():
                raise forms.ValidationError("No puedes reservar para el mismo día.")
            if data["fecha_inicio"] < now:
                raise forms.ValidationError("La fecha no puede ser pasada.")
        return data

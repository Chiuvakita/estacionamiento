from django import forms
from django.utils import timezone
from ..models.reserva import Reserva
from apps.vehiculos.models import Vehiculo

class ReservaCrearForm(forms.Form):
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(),
        label="Vehículo",
        empty_label="Selecciona un vehículo"
    )
    estacionamiento_id = forms.IntegerField(label="Estacionamiento")
    fecha_inicio = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])
    duracion = forms.IntegerField(min_value=1, label="Duración (horas)")

    def clean(self):
        data = super().clean()
        if "fecha_inicio" in data and data["fecha_inicio"] is not None:
            now = timezone.now()
            if data["fecha_inicio"].date() == now.date():
                raise forms.ValidationError("No puedes reservar para el mismo día.")
            if data["fecha_inicio"] < now:
                raise forms.ValidationError("La fecha no puede ser pasada.")
        return data

from django import forms
from django.utils import timezone
from datetime import timedelta
from apps.vehiculos.models import Vehiculo
from apps.estacionamientos.models.estacionamiento import Estacionamiento

class ReservaCrearForm(forms.Form):
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(),
        label="Vehículo",
        empty_label="Selecciona un vehículo"
    )

    estacionamiento = forms.ModelChoiceField(
        queryset=Estacionamiento.objects.filter(estado="D"),
        label="Estacionamiento",
        empty_label="Selecciona un estacionamiento"
    )

    fecha_inicio = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    duracion = forms.IntegerField(min_value=1, label="Duración (horas)")

    def clean(self):
        data = super().clean()

        fecha = data.get("fecha_inicio")
        if not fecha:
            return data

        # Convertir naive → aware
        if timezone.is_naive(fecha):
            fecha = timezone.make_aware(fecha, timezone.get_current_timezone())
            data["fecha_inicio"] = fecha

        now = timezone.localtime()
        minimo = now + timedelta(hours=2)

        if fecha < minimo:
            raise forms.ValidationError(
                f"Debes reservar con al menos 2 horas de anticipación. "
                f"Hora mínima permitida: {minimo.strftime('%d/%m %H:%M')}"
            )

        return data

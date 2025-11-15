from django.db import models
from apps.estacionamientos.models.estacionamiento import Estacionamiento
from apps.vehiculos.models import Vehiculo

class Historial(models.Model):
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.SET_NULL)

    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField(null=True, blank=True)
    es_reserva = models.BooleanField(default=False)

    def __str__(self):
        return f"Historial Estac {self.estacionamiento_id} • {self.fecha_inicio.strftime('%Y-%m-%d %H:%M')}"

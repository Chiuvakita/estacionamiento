from django.db import models
from django.utils import timezone

class Reserva(models.Model):
    estacionamiento = models.ForeignKey("estacionamientos.Estacionamiento", on_delete=models.CASCADE)
    patente = models.CharField(max_length=20, default="DESCONOCIDA")
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_termino = models.DateTimeField(null=True, blank=True)
    tipo_snapshot = models.CharField(max_length=20, default="Normal")

    def duracion_horas(self) -> int:
        if self.fecha_termino and self.fecha_inicio:
            diff = self.fecha_termino - self.fecha_inicio
            return int(diff.total_seconds() // 3600)
        return 0

    @property
    def tiempo_restante(self) -> str:
        ahora = timezone.now()
        if self.fecha_termino and self.fecha_termino > ahora:
            diff = self.fecha_termino - ahora
            horas = diff.seconds // 3600
            minutos = (diff.seconds % 3600) // 60
            return f"{horas}h {minutos}m"
        return "Finalizada"

    def __str__(self):
        return f"Reserva {self.pk} • {self.patente}"

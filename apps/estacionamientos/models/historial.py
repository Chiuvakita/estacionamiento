from django.db import models

class Historial(models.Model):
    estacionamiento = models.ForeignKey("estacionamientos.Estacionamiento", on_delete=models.CASCADE)
    patente = models.CharField(max_length=20)
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField(null=True, blank=True)
    es_reserva = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.estacionamiento} • {self.patente} • {self.fecha_inicio.strftime('%Y-%m-%d %H:%M')}"

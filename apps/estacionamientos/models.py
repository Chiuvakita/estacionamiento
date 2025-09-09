from django.db import models
from django.utils import timezone


class Estacionamiento(models.Model):
    ESTADO_CHOICES = [
        ("D", "Disponible"),
        ("O", "Ocupado"),
    ]
    TIPO_CHOICES = [
        ("Normal", "Normal"),
        ("VIP", "VIP"),
        ("Discapacitado", "Discapacitado"),
    ]

    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default="D")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="Normal")

    patente = models.CharField(max_length=10, null=True, blank=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_termino = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Estac #{self.pk} - {self.get_estado_display()} ({self.tipo})"


class Reserva(models.Model):
    estacionamiento = models.ForeignKey("Estacionamiento", on_delete=models.CASCADE)
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


class Historial(models.Model):
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)
    patente = models.CharField(max_length=20)
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField(null=True, blank=True)
    es_reserva = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.estacionamiento} • {self.patente} • {self.fecha_inicio.strftime('%Y-%m-%d %H:%M')}"

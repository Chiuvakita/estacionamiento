from django.db import models

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

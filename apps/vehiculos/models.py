from django.db import models

class Vehiculo(models.Model):
    patente = models.CharField(
        max_length=6,
        unique=True,
        error_messages={'unique': 'Ya existe un vehículo con esta patente.'}
    )
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.patente} - {self.marca} {self.modelo}"

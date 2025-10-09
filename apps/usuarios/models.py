from django.db import models


class Usuario(models.Model):
    rut = models.IntegerField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=45)
    apellidoPaterno = models.CharField(max_length=45)
    apellidoMaterno = models.CharField(max_length=45)
    numeroTelefono = models.CharField(max_length=45)
    rol = models.CharField(max_length=45)
    discapacidad = models.BooleanField()

    def __str__(self):
        return f"{self.nombre} {self.apellidoPaterno} {self.apellidoMaterno} {self.rol} {self.discapacidad}"
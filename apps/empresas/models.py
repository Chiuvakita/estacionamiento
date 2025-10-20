from django.db import models

#Crear modelo de django para almacenar la información
#No se agrega id porque django ya trabaja con sus propios ids autoincrementales
#No se agrega encapsulamiento ya que django necesita acceder a los datos de forma pública

class Empresa(models.Model):
    nombre = models.CharField(max_length=300)
    telefono = models.CharField(max_length=45)
    correo = models.EmailField(max_length=254)
    direccion = models.CharField(max_length=300)
    
class Sucursal(models.Model):
    cantidadEstacionamiento = models.IntegerField()
    nombreSucursal = models.CharField(max_length=100)
    direccion = models.CharField(max_length=300)
    numero = models.CharField(max_length=45)

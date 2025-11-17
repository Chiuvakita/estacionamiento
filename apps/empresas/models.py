from django.db import models

#Crear modelo de django para almacenar la información
#No se agrega id porque django ya trabaja con sus propios ids autoincrementales
#No se agrega encapsulamiento ya que django necesita acceder a los datos de forma pública
#Finalmente se agrega la relación entre empresa y sucursal

class Empresa(models.Model):
    nombre = models.CharField(max_length=300)
    telefono = models.CharField(max_length=45)
    correo = models.EmailField(max_length=254)
    direccion = models.CharField(max_length=300)

    def __str__(self):
        return f" Empresa: {self.nombre} \n Telefono: {self.telefono} \n Correo: {self.correo} \n Direccion: {self.direccion}"

    
class Sucursal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default=None)
    cantidadEstacionamiento = models.IntegerField()
    nombreSucursal = models.CharField(max_length=100)
    direccion = models.CharField(max_length=300)
    numero = models.CharField(max_length=45)

    def __str__(self):
        return f" Empresa: {self.empresa} \n Sucursal: {self.nombreSucursal} \n Direccion: {self.direccion} \n Numero: {self.numero} \n Cantidad de estacionamiento: {self.cantidadEstacionamiento}"

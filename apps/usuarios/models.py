from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    ROLES = [
        ("Administrador", "Administrador"),
        ("Empleado", "Empleado"),
        ("Cliente", "Cliente"),
    ]

    rut = models.IntegerField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=45)
    apellidoPaterno = models.CharField(max_length=45)
    apellidoMaterno = models.CharField(max_length=45)
    numeroTelefono = models.CharField(max_length=45)
    clave = models.CharField(max_length=130, default="")
    rol = models.CharField(max_length=45, choices=ROLES, default="Cliente")
    discapacidad = models.BooleanField(default=False)

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def esAdministrador(self):
        return self.rol == "Administrador"
    def esEmpleado(self):
        return self.rol == "Empleado"
    def esCliente(self):
        return self.rol == "Cliente"
    
    def puedeGestionar(self):
        return self.rol in ["Administrador", "Empleado"]
    
    def setClave(self, claveSinHash):
        self.clave = make_password(claveSinHash)
    
    def checkClave(self, claveSinHash):
        return check_password(claveSinHash, self.clave)
    def __str__(self):
        return f"{self.nombre} {self.apellidoPaterno} {self.apellidoMaterno} {self.rol} {self.discapacidad}"
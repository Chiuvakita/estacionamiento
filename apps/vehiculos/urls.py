from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_vehiculos, name="vehiculos_listar"),
]



# Definir ruta listarVehiculo
# Definir ruta crearVehiculo
# Definir ruta editarVehiculo
# Definir ruta eliminarVehiculo

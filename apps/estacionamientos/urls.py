from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_estacionamientos, name="estacionamientos_listar"),
]


# Definir ruta listarEstacionamiento
# Definir ruta crearEstacionamiento
# Definir ruta editarEstacionamiento
# Definir ruta eliminarEstacionamiento

# Definir ruta listarReserva
# Definir ruta crearReserva
# Definir ruta terminarReserva

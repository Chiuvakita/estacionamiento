from django.urls import path

from .views.home import home, marcarSalida, marcarSalidaPatente
from .views.estacionamientos import (
    listarEstacionamiento, crearEstacionamiento, crearEstacionamientosMasivo,
    editarEstacionamiento, eliminarEstacionamiento, eliminarTodosEstacionamientos,
)
from .views.reservas import listarReserva, crearReserva, terminarReserva
from .views.historial import listarHistorial

urlpatterns = [
    # Home 
    path("", home, name="home"),
    path("salida/<int:id>/", marcarSalida, name="marcarSalida"),
    path("salida_por_patente/", marcarSalidaPatente, name="marcarSalidaPatente"),

    # CRUD Estacionamientos
    path("estacionamientos/", listarEstacionamiento, name="listarEstacionamiento"),
    path("estacionamientos/crear/", crearEstacionamiento, name="crearEstacionamiento"),
    path("estacionamientos/crear_masivo/", crearEstacionamientosMasivo, name="crearEstacionamientosMasivo"),
    path("estacionamientos/<int:id>/editar/", editarEstacionamiento, name="editarEstacionamiento"),
    path("estacionamientos/<int:id>/eliminar/", eliminarEstacionamiento, name="eliminarEstacionamiento"),
    path("estacionamientos/eliminar_todos/", eliminarTodosEstacionamientos, name="eliminarTodosEstacionamientos"),

    # Reservas
    path("reservas/", listarReserva, name="listarReserva"),
    path("reservas/crear/", crearReserva, name="crearReserva"),
    path("reservas/<int:id>/terminar/", terminarReserva, name="terminarReserva"),

    # Historial
    path("historial/", listarHistorial, name="listarHistorial"),
]

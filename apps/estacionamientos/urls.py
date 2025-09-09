from django.urls import path
from . import views

urlpatterns = [
    # Home 
    path("", views.home, name="home"),
    path("salida/<int:id>/", views.marcarSalida, name="marcarSalida"),
    path("salida_por_patente/", views.marcarSalidaPatente, name="marcarSalidaPatente"),

    # CRUD Estacionamientos
    path("estacionamientos/", views.listarEstacionamiento, name="listarEstacionamiento"),
    path("estacionamientos/crear/", views.crearEstacionamiento, name="crearEstacionamiento"),
    path("estacionamientos/crear_masivo/", views.crearEstacionamientosMasivo, name="crearEstacionamientosMasivo"),
    path("estacionamientos/<int:id>/editar/", views.editarEstacionamiento, name="editarEstacionamiento"),
    path("estacionamientos/<int:id>/eliminar/", views.eliminarEstacionamiento, name="eliminarEstacionamiento"),
    path("estacionamientos/eliminar_todos/", views.eliminarTodosEstacionamientos, name="eliminarTodosEstacionamientos"),

    # Reservas
    path("reservas/", views.listarReserva, name="listarReserva"),
    path("reservas/crear/", views.crearReserva, name="crearReserva"),
    path("reservas/<int:id>/terminar/", views.terminarReserva, name="terminarReserva"),

    path("historial/", views.listarHistorial, name="listarHistorial"),
]

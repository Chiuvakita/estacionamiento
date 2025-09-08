from django.urls import path
from . import views

urlpatterns = [
    # ====================
    # HOME
    # ====================
    path("", views.home, name="home"),
    path("marcarSalidaPatente/", views.marcarSalidaPatente, name="marcarSalidaPatente"),

    # ====================
    # ESTACIONAMIENTOS (Admin)
    # ====================
    path("estacionamientos/", views.listarEstacionamiento, name="listarEstacionamiento"),
    path("estacionamientos/crear/", views.crearEstacionamiento, name="crearEstacionamiento"),
    path("estacionamientos/crearMasivo/", views.crearEstacionamientosMasivo, name="crearEstacionamientosMasivo"),
    path("estacionamientos/editar/<int:id>/", views.editarEstacionamiento, name="editarEstacionamiento"),
    path("estacionamientos/eliminar/<int:id>/", views.eliminarEstacionamiento, name="eliminarEstacionamiento"),
    path("estacionamientos/marcarSalida/<int:id>/", views.marcarSalida, name="marcarSalida"),
    path("estacionamientos/eliminarTodos/", views.eliminarTodosEstacionamientos, name="eliminarTodosEstacionamientos"),

    # ====================
    # RESERVAS (Cliente)
    # ====================
    path("reservas/", views.listarReserva, name="listarReserva"),
    path("reservas/crear/", views.crearReserva, name="crearReserva"),
    path("reservas/terminar/<int:id>/", views.terminarReserva, name="terminarReserva"),

    # ====================
    # HISTORIAL
    # ====================
    path("historial/", views.listarHistorial, name="listarHistorial"),
]

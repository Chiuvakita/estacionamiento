from django.urls import path
from . import views

urlpatterns = [
    # Estacionamientos
    path("", views.listar_estacionamiento, name="estacionamientos_listar"),
    path("crear/", views.crear_estacionamiento, name="estacionamiento_crear"),
    path("editar/<int:id>/", views.editar_estacionamiento, name="editar_estacionamiento"),
    path("eliminar/<int:id>/", views.eliminar_estacionamiento, name="estacionamiento_eliminar"),

    # Reservas
    path("reservas/", views.listar_reserva, name="reservas_listar"),
    path("reservas/crear/", views.crear_reserva, name="reserva_crear"),
    path("reservas/terminar/<int:id>/", views.terminar_reserva, name="reserva_terminar"),

    # Main (admin)
    path("main/ingreso/", views.main_ingreso, name="main_ingreso"),
]


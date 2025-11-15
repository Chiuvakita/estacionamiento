from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar, name="listarVehiculos"),
    path("crear/", views.crear, name="crearVehiculo"),
    path("editar/<int:id>/", views.editar, name="editarVehiculo"),
    path("eliminar/<int:id>/", views.eliminar, name="eliminarVehiculo"),
    path("eliminar-todos/", views.eliminar_todos, name="eliminarTodosVehiculos"),
]

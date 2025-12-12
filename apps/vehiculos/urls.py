from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import VehiculoViewSet

enrutador = DefaultRouter()
enrutador.register(r'api/vehiculos', VehiculoViewSet, basename='vehiculo')

urlpatterns = [
    path("", views.listar, name="listarVehiculos"),
    path("crear/", views.crear, name="crearVehiculo"),
    path("editar/<int:id>/", views.editar, name="editarVehiculo"),
    path("eliminar/<int:id>/", views.eliminar, name="eliminarVehiculo"),
    path("eliminar-todos/", views.eliminarTodos, name="eliminarTodosVehiculos"),
    
    path('', include(enrutador.urls)),
]

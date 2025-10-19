from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarVehiculos, name='listarVehiculos'),
    path('crear/', views.crearVehiculo, name='crearVehiculo'),
    path('editar/<int:id>/', views.editarVehiculo, name='editarVehiculo'),
    path('eliminar/<int:id>/', views.eliminarVehiculo, name='eliminarVehiculo'),
    path('eliminar_todos/', views.eliminarTodosVehiculos, name='eliminarTodosVehiculos'),
]

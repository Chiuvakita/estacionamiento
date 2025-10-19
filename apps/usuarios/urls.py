from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crearUsuarios, name="crearUsuarios"),
    path("", views.listarUsuarios, name="listarUsuarios"),
    path('editar/<int:rut>', views.editarUsuario, name='editarUsuario'),
    path('eliminar/<int:rut>', views.eliminarUsuario, name='eliminarUsuario'),
    path('registro/', views.registroView, name='registro'),
]



# Definir ruta listarUsuarios
# Definir ruta crearUsuario
# Definir ruta editarUsuario
# Definir ruta eliminarUsuario

# Definir ruta crearCredencial
# Definir ruta editarCredencial
# Definir ruta eliminarCredencial

from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_usuarios, name="usuarios_listar"),
]



# Definir ruta listarUsuarios
# Definir ruta crearUsuario
# Definir ruta editarUsuario
# Definir ruta eliminarUsuario

# Definir ruta crearCredencial
# Definir ruta editarCredencial
# Definir ruta eliminarCredencial

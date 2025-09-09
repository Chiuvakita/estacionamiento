from django.urls import path
from . import views

urlpatterns = [
    path("", views.listarEmpresa, name="empresas_listar"),
    path("crearEmpresa/", views.crearEmpresa, name="crearEmpresa")
]


# Definir ruta listarEmpresa
# Definir ruta crearEmpresa
# Definir ruta editarEmpresa
# Definir ruta eliminarEmpresa

# Definir ruta listarSucursal
# Definir ruta crearSucursal
# Definir ruta editarSucursal
# Definir ruta eliminarSucursal

# Definir ruta asociarUsuarioSucursal

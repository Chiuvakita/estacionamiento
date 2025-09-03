from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_empresas, name="empresas_listar"),
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

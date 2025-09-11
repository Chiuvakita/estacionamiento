from django.urls import path
from . import views

urlpatterns = [
    path("", views.listarEmpresa, name="empresas_listar"),
    path("crearEmpresa/", views.crearEmpresa, name="crearEmpresa"),# Definir ruta crearEmpresa
    path("listarEmpresa/", views.listarEmpresa, name="listarEmpresa"),# Definir ruta listarEmpresa
    path("editarEmpresa/<int:empresa_id>/", views.editarEmpresa, name="editarEmpresa"),# Definir ruta editarEmpresa
    path("eliminarEmpresa/<int:empresa_id>/", views.eliminarEmpresa, name="eliminarEmpresa"),# Definir ruta eliminarEmpresa
]







# Definir ruta listarSucursal
# Definir ruta crearSucursal
# Definir ruta editarSucursal
# Definir ruta eliminarSucursal

# Definir ruta asociarUsuarioSucursal

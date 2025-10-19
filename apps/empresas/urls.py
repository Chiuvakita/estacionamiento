from django.urls import path
from . import views

urlpatterns = [
    path("", views.listarEmpresa, name="empresas_listar"),
    path("crearEmpresa/", views.gestionarEmpresa, name="crearEmpresa"),# Definir ruta crearEmpresa
    path("listarEmpresa/", views.listarEmpresa, name="listarEmpresa"),# Definir ruta listarEmpresa
    path("editarEmpresa/<int:empresa_id>/", views.gestionarEmpresa, name="editarEmpresa"),# Definir ruta editarEmpresa
    path("eliminarEmpresa/<int:empresa_id>/", views.eliminarEmpresa, name="eliminarEmpresa"),# Definir ruta eliminarEmpresa
    
    path("crearSucursal/", views.gestionarSucursal, name="crearSucursal"),
    path("listarSucursal/", views.listarSucursal, name="listarSucursal"),
    path("editarSucursal/<int:sucursal_id>/", views.gestionarSucursal, name="editarSucursal"),
    path("eliminarSucursal/<int:sucursal_id>/", views.eliminarSucursal, name="eliminarSucursal")
]







# Definir ruta listarSucursal
# Definir ruta crearSucursal
# Definir ruta editarSucursal
# Definir ruta eliminarSucursal

# Definir ruta asociarUsuarioSucursal
